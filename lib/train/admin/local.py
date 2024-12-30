class EnvironmentSettings:
    def __init__(self):
        self.workspace_dir = '/home/hxt/code/STTrack_pub'    # Base directory for saving network checkpoints.
        self.tensorboard_dir = '/nasdata/tracking/hxt/STTrack_pub/tensorboard'    # Directory for tensorboard files.
        self.pretrained_networks = '/nasdata/tracking/hxt/STTrack_pub/pretrained_networks'
        self.got10k_val_dir = '/nasdata/tracking/hxt/STTrack_pub/data/got10k/val'
        self.lasot_lmdb_dir = '/nasdata/tracking/hxt/STTrack_pub/data/lasot_lmdb'
        self.got10k_lmdb_dir = '/nasdata/tracking/hxt/STTrack_pub/data/got10k_lmdb'
        self.trackingnet_lmdb_dir = '/nasdata/tracking/hxt/STTrack_pub/data/trackingnet_lmdb'
        self.coco_lmdb_dir = '/nasdata/tracking/hxt/STTrack_pub/data/coco_lmdb'
        self.coco_dir = '/nasdata/tracking/hxt/STTrack_pub/data/coco'
        self.lasot_dir = '/nasdata/tracking/hxt/STTrack_pub/data/lasot'
        self.got10k_dir = '/nasdata/tracking/hxt/STTrack_pub/data/got10k/train'
        self.trackingnet_dir = '/nasdata/tracking/hxt/STTrack_pub/data/trackingnet'
        self.depthtrack_dir = '/nasdata/tracking/data/DepthTrack/train'
        self.lasher_dir = '/nasdata/tracking/data/LasHeR/trainingset'
        self.visevent_dir = '/nasdata/tracking/data/VisEvent/train_subset'
