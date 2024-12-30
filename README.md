# Exploiting Multimodal Spatial-temporal Patterns for Video Object Tracking [AAAI2025]
Official implementation of [**STTrack**](https://arxiv.org/abs/2412.15691), including models and training&testing codes.

[Models & Raw Results](https://drive.google.com/drive/folders/1k7_S0AAyMFSBAem87AJhLjg8Sq1v5VgN?usp=drive_link)(Google Driver) [Models & Raw Results](https://pan.baidu.com/s/1TR4qnWtXS140pddngcn_-w 
)(Baidu Driver:9527)


## News
**[Dec 30, 2024]**
- We release codes, models and raw results. Thanks for your star.


## Introduction
- A new unified multimodal spatial-temporal tracking framework (e.g. RGB-D, RGB-T, and RGB-E Tracking).

- STTrack excels in multiple multimodal tracking tasks. We hope it will garner more attention for multimodal tracking.


<center><img width="90%" alt="" src="assets/structure.png"/></center>

 <!-- Results -->


<!-- <<<<<<< HEAD
<!-- ### On RGB-T tracking benchmarks
=======
### On RGB-T tracking benchmarks
>>>>>>> e04a44192a1d1e1e30a4a9a9c234b8adc5bddf8a
<div style="text-align:center;">
  <img width="50%" alt="" src="assets/results_rgbt.png"/> -->
## Strong Performance
| Tracker | LasHeR | RGBT234 | VisEvent | DepthTrack | VOT22RGBD|
|:-----------:|:------------:|:-----------:|:-----------------:|:-----------:|:-----------:|
| STTrack | 60.3 | 66.7 | 61.9 |  77.6 | 63.3 | 


<!-- =======
</div>
>>>>>>> e04a44192a1d1e1e30a4a9a9c234b8adc5bddf8a -->

## Usage
### Installation
Create and activate a conda environment:
```
conda create -n STTrack python=3.8
conda activate STTrack
```
Install the required packages:
```
bash install_sttrack.sh
```

### Data Preparation
Put the training datasets in ./data/. It should look like:
```
$<PATH_of_STTrack>
-- data
    -- DepthTrackTraining
        |-- adapter02_indoor
        |-- bag03_indoor
        |-- bag04_indoor
        ...
    -- LasHeR/train/trainingset
        |-- 1boygo
        |-- 1handsth
        ...
    -- VisEvent/train
        |-- 00142_tank_outdoor2
        |-- 00143_tank_outdoor2
        ...
        |-- trainlist.txt
```

### Path Setting
Run the following command to set paths:
```
cd <PATH_of_STTrack>
python tracking/create_default_local_file.py --workspace_dir . --data_dir ./data --save_dir ./output
```
You can also modify paths by these two files:
```
./lib/train/admin/local.py  # paths for training
./lib/test/evaluation/local.py  # paths for testing
```

### Training
Dowmload the pretrained [foundation model](https://drive.google.com/drive/folders/1ttafo0O5S9DXK2PX0YqPvPrQ-HWJjhSy?usp=sharing) (OSTrack) 
and put it under ./pretrained/.
```
bash train.sh
```
You can train models with various modalities and variants by modifying ```train.sh```.

### Testing
#### For RGB-D benchmarks
[DepthTrack Test set & VOT22_RGBD]\
These two benchmarks are evaluated using [VOT-toolkit](https://github.com/votchallenge/toolkit). \
You need to put the DepthTrack test set to```./Depthtrack_workspace/``` and name it 'sequences'.\
You need to download the corresponding test sequences at```./vot22_RGBD_workspace/```.

```
bash test_rgbd.sh
```

#### For RGB-T benchmarks
[LasHeR & RGBT234] \
Modify the <DATASET_PATH> and <SAVE_PATH> in```./RGBT_workspace/test_rgbt_mgpus.py```, then run:
```
bash test_rgbt.sh
```
We refer you to [LasHeR Toolkit](https://github.com/BUGPLEASEOUT/LasHeR) for LasHeR evaluation, 
and refer you to [MPR_MSR_Evaluation](https://sites.google.com/view/ahutracking001/) for RGBT234 evaluation.


#### For RGB-E benchmark
[VisEvent]\
Modify the <DATASET_PATH> and <SAVE_PATH> in```./RGBE_workspace/test_rgbe_mgpus.py```, then run:
```
bash test_rgbe.sh
```
We refer you to [VisEvent_SOT_Benchmark](https://github.com/wangxiao5791509/VisEvent_SOT_Benchmark) for evaluation.


## Bixtex
If you find STTrack is helpful for your research, please consider citing:

```bibtex
@inproceedings{STTrack,
  title={Exploiting Multimodal Spatial-temporal Patterns for Video Object Tracking},
  author={Xiantao, Hu and Ying, Tai and Xu, Zhao and Chen, Zhao and Zhenyu, Zhang and Jun, Li and Bineng, Zhong and Jian, Yang},
  booktitle={AAAI},
  year={2025}
}
```

## Acknowledgment
- This repo is based on [OSTrack](https://github.com/botaoye/OSTrack) and [ViPT](https://github.com/jiawen-zhu/ViPT) which are an excellent work.
- We thank for the [PyTracking](https://github.com/visionml/pytracking) library, which helps us to quickly implement our ideas.

