all:


run:
	LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 ./src/main.py

view:
	LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 ./src/view/view_camera.py


find_goal:
	LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 ./src/tracking/test_tracking.py

track:
	LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 python3 ./src/tracking/ball_tracking.py

deps: deps-no-pip deps-pip

deps-no-pip:
	sudo apt-get install -y build-essential cmake git pkg-config
	sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
	sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
	sudo apt-get install -y libgtk2.0-dev libcanberra-gtk-module
	sudo apt-get install -y libatlas-base-dev gfortran
	sudo apt-get install -y libhdf5-103
	sudo apt-get install -y libqtgui
	sudo apt-get install -y libqt4-test
	sudo apt-get install -y python3-pip


deps-pip:
	python3 -m pip install --user RPi.GPIO imutils numpy matplotlib pandas opencv-contrib-python


test_control:
	python3 src/control/test_control.py
