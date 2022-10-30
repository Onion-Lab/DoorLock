# dlib 설치
pip3 install dlib

# 만약 안되면
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build; cd build; cmake ..; cmake --build .
cd ..
python3 setup.py install

# face_recognition, opencv 모듈 설치
pip3 install face_recognition python3-opencv

# pi camera 켜기(안하면 OpenCV의 VideoCapture 사용 불가
sudo raspi-config 명령 ->  legacy camera 켜기

# 데몬화
1. Doorlock 폴더를 라즈베리파이의 /home/pi에 복사한다.
2. demon_setup.sh를 실행한다.