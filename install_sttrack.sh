echo "****************** Installing pytorch ******************"
#conda install -y pytorch==1.7.0 torchvision==0.8.1 cudatoolkit=10.2 -c pytorch
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia -y
echo ""
echo ""
echo "****************** Installing yaml ******************"
pip install PyYAML

echo ""
echo ""
echo "****************** Installing easydict ******************"
pip install easydict

echo ""
echo ""
echo "****************** Installing cython ******************"
pip install cython

echo ""
echo ""
echo "****************** Installing opencv-python ******************"
pip install opencv-python

echo ""
echo ""
echo "****************** Installing pandas ******************"
pip install pandas

echo ""
echo ""
echo "****************** Installing tqdm ******************"
conda install -y tqdm

echo ""
echo ""
echo "****************** Installing coco toolkit ******************"
pip install pycocotools

echo ""
echo ""
echo "****************** Installing jpeg4py python wrapper ******************"
apt-get install libturbojpeg
pip install jpeg4py

echo ""
echo ""
echo "****************** Installing scipy ******************"
pip install scipy

echo ""
echo ""
echo "****************** Installing timm ******************"
pip install timm==0.5.4

echo ""
echo ""
echo "****************** Installing tensorboard ******************"
pip install tb-nightly

echo ""
echo ""
echo "****************** Installing lmdb ******************"
pip install lmdb

echo ""
echo ""
echo "****************** Installing visdom ******************"
pip install visdom

echo ""
echo ""
echo "****************** Installing vot-toolkit python ******************"
pip install git+https://github.com/votchallenge/vot-toolkit-python

echo "****************** Installing mamba ******************"
cd ./mamba_install/causal-conv1d && pip install . && cd ../.. # recommended to use sudo
cd ./mamba_install/mamba-1p1p1 && pip install . && cd ../..  # recommended to use sudo
cd ./mamba_install/selective_scan && pip install . && cd ../.. # recommended to use sudo

echo "****************** Installation complete! ******************"
