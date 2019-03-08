sudo pip install sklearn numpy scikit-image flask flask-socketio

cd ml
git clone https://github.com/davidsandberg/facenet.git facenet_repo
cd facenet_repo
git checkout 096ed77
cd ..
mkdir weights
cd weights

python ../../googledrive_download.py 1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55- 20180402-114759.zip
unzip 20180402-114759.zip
rm
cd ..
