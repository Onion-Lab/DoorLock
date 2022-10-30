sudo cp face-doorlock-server.service /etc/systemd/system/
sudo cp face-doorlock.service /etc/systemd/system/

sudo systemctl enable face-doorlock-server
sudo systemctl enable face-doorlock
