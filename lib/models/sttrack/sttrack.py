import math
from operator import ipow
import os
from typing import List

import torch
from torch import nn
from torch.nn.modules.transformer import _get_clones

from lib.models.layers.head import build_box_head, conv
from lib.models.sttrack.vit_care import vit_base_patch16_224
from lib.utils.box_ops import box_xyxy_to_cxcywh
from lib.models.layers.mamba import TSGBlock, MambaFusionBlock

class STTrack(nn.Module):
    """ This is the base class for STTrack developed on OSTrack (Ye et al. ECCV 2022) """

    def __init__(self, transformer, box_head, cfg, aux_loss=False, head_type="CORNER"):
        """ Initializes the model.
        Parameters:
            transformer: torch module of the transformer architecture.
            aux_loss: True if auxiliary decoding losses (loss at each decoder layer) are to be used.
        """
        super().__init__()
        hidden_dim = transformer.embed_dim
        self.backbone = transformer
        self.decode_fuse_search = conv(hidden_dim, hidden_dim)  # Fuse RGB and T search regions, random initialized
        self.box_head = box_head
        self.TSG_layer = cfg.MODEL.TSG.LAYER
        self.track_query_len = cfg.MODEL.TSG.TRACK_QUERY
        self.track_beforequery_len = cfg.MODEL.TSG.TRACK_QUERY_OLD
        self.template_number = cfg.DATA.TEMPLATE.NUMBER

        self.TSG = nn.ModuleList([
             TSGBlock(
                hidden_dim=hidden_dim,
                mlp_ratio=0.0,
                d_state=128,
            )
            for i in range(self.TSG_layer)])
        
        self.MambaFusion = MambaFusionBlock(  
                hidden_dim=hidden_dim ,
                mlp_ratio=0.0,
                d_state=256,
            )

        self.aux_loss = aux_loss
        self.head_type = head_type
        if head_type == "CORNER" or head_type == "CENTER":
            self.feat_sz_s = int(box_head.feat_sz)
            self.feat_len_s = int(box_head.feat_sz ** 2)

        if self.aux_loss:
            self.box_head = _get_clones(self.box_head, 6)
        
    def forward(self, template: torch.Tensor,
                search: torch.Tensor,
                ce_template_mask=None,
                return_last_attn=False,
                track_query_before = None,
                keep_rate=None,
                ):
        track_query_before = track_query_before
        out_dict = []
        for i in range(len(search)):
            if track_query_before == None:
                track_query_before =  [nn.Parameter(torch.zeros(1,self.track_beforequery_len,self.backbone.embed_dim)).to('cuda') for i in range(2)]
                
            x, aux_dict,len_zx = self.backbone(z=template, x=search[i],track_query_before = track_query_before,
                                        keep_rate=keep_rate,
                                        ce_template_mask=ce_template_mask,
                                        return_last_attn=return_last_attn, )
            num_template_token = len_zx[0]
            num_search_token = len_zx[1]

            B,N,_ = x.size()
           
            track_query_now = [ nn.Parameter(torch.zeros(B,self.track_query_len,self.backbone.embed_dim)).to('cuda') for i in range(2)]

            temp_x = x[:, :N//2, :]
            temp_r = x[:, N//2:, :]

                
            track_query_now_x = track_query_now[0]
            track_query_now_r = track_query_now[1]
            temp_x = torch.cat([ temp_x, track_query_now_x],dim=1)
            temp_r = torch.cat([temp_r, track_query_now_r],dim=1)

            for i in range(self.TSG_layer):
                temp_x_flip =  temp_x
                temp_x_flip[:,:-(self.track_query_len+self.track_beforequery_len),:] = temp_x_flip[:,:-(self.track_query_len+self.track_beforequery_len),:].flip(dims=[1])

                temp_r_flip =  temp_r
                temp_r_flip[:,:-(self.track_query_len+self.track_beforequery_len),:] = temp_r_flip[:,:-(self.track_query_len+self.track_beforequery_len),:].flip(dims=[1])

                temp_x, temp_r = self.TSG[i](temp_x,temp_r)
                temp_x_flip, temp_r_flip = self.TSG[i](temp_x_flip,temp_r_flip)
                
                temp_x_flip[:,:-(self.track_query_len+self.track_beforequery_len),:]= temp_x_flip[:,:-(self.track_query_len+self.track_beforequery_len),:].flip(dims=[1])
                temp_r_flip[:,:-(self.track_query_len+self.track_beforequery_len),:]= temp_r_flip[:,:-(self.track_query_len+self.track_beforequery_len),:].flip(dims=[1])

                temp_x = temp_x +  temp_x_flip
                temp_r = temp_r +  temp_r_flip

            track_query_now_x = temp_x[:,-self.track_query_len:,:]
            track_query_now_r = temp_r[:,-self.track_query_len:,:]
            track_query_before[0] = track_query_before[0][:,:-1]
            track_query_before[1] = track_query_before[1][:,:-1]
            if track_query_before[0].size(0) != B:
                track_query_before[0] = track_query_before[0].expand(B,-1,-1)
                track_query_before[1] = track_query_before[1].expand(B,-1,-1)
            track_query_before[0] = torch.cat([track_query_before[0],track_query_now_x],dim=1)
            track_query_before[1] = torch.cat([track_query_before[1],track_query_now_r],dim=1)
            
            
            temp_x = temp_x[:,:-(self.track_query_len+self.track_beforequery_len),:]
            temp_r = temp_r[:,:-(self.track_query_len+self.track_beforequery_len),:]

            feat_last = self.MambaFusion(temp_x,temp_r)[:,-num_search_token:,:]

            out = self.forward_head(feat_last, None)
            out.update(aux_dict)
            out['track_query_before'] = track_query_before
            out['backbone_feat'] = x
            out_dict.append(out)
        return out_dict

    def forward_head(self, cat_feature ,gt_score_map=None):
        """
        cat_feature: output embeddings of the backbone, it can be (HW1+HW2, B, C) or (HW2, B, C)
        """

        opt = (cat_feature.unsqueeze(-1)).permute((0, 3, 2, 1)).contiguous()
        bs, Nq, C, HW = opt.size()
        HW = int(HW/2)
        opt_feat = opt.view(-1, C, self.feat_sz_s, self.feat_sz_s)
        opt_feat = self.decode_fuse_search(opt_feat)

        if self.head_type == "CORNER":
            # run the corner head
            pred_box, score_map = self.box_head(opt_feat, True)
            outputs_coord = box_xyxy_to_cxcywh(pred_box)
            outputs_coord_new = outputs_coord.view(bs, Nq, 4)
            out = {'pred_boxes': outputs_coord_new,
                   'score_map': score_map,
                   }
            return out
        elif self.head_type == "CENTER":
            # run the center head
            score_map_ctr, bbox, size_map, offset_map = self.box_head(opt_feat, gt_score_map)
            # outputs_coord = box_xyxy_to_cxcywh(bbox)
            outputs_coord = bbox
            outputs_coord_new = outputs_coord.view(bs, Nq, 4)
            out = {'pred_boxes': outputs_coord_new,
                   'score_map': score_map_ctr,
                   'size_map': size_map,
                   'offset_map': offset_map}
            return out
        else:
            raise NotImplementedError


def build_sttrack(cfg, training=True):
    current_dir = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
    pretrained_path = os.path.join(current_dir, '../../../pretrained')
    if cfg.MODEL.PRETRAIN_FILE and ('STTrack' not in cfg.MODEL.PRETRAIN_FILE) and training:
        pretrained = os.path.join(pretrained_path, cfg.MODEL.PRETRAIN_FILE)
        print('Load pretrained model from: ' + pretrained)
    else:
        pretrained = ''

    if cfg.MODEL.BACKBONE.TYPE == 'vit_base_patch16_224':
        backbone = vit_base_patch16_224(pretrained, drop_path_rate=cfg.TRAIN.DROP_PATH_RATE,
                                            cross_loc=cfg.MODEL.BACKBONE.CROSS_LOC,
                                            drop_path=cfg.TRAIN.CROSS_DROP_PATH,
                                            )
    else:
        raise NotImplementedError

    hidden_dim = backbone.embed_dim
    patch_start_index = 1

    backbone.finetune_track(cfg=cfg, patch_start_index=patch_start_index)

    box_head = build_box_head(cfg, hidden_dim)

    model = STTrack(
        backbone,
        box_head,
        cfg,
        aux_loss=False,
        head_type=cfg.MODEL.HEAD.TYPE,
    )

    if 'SOT' in cfg.MODEL.PRETRAIN_FILE and training:
        pretrained_file = os.path.join(pretrained_path, cfg.MODEL.PRETRAIN_FILE)
        checkpoint = torch.load(pretrained_file, map_location="cpu")
        missing_keys, unexpected_keys = model.load_state_dict(checkpoint["net"], strict=False)
        print('Load pretrained model from: ' + cfg.MODEL.PRETRAIN_FILE)

    return model
