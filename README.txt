# install python 3.4
sudo apt-get install python3.4
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3.4 get-pip.py
sudo pip3.4 install beautifulsoup4
sudo pip3.4 install lxml
sudo pip3.4 install keras
sudo pip3.4 install tensorflow

# split the data training/cross validation
sudo pip3.4 install -U scikit-learn

# plot graphs
sudo pip3.4 install matplotlib
sudo apt-get install python3-matplotlib
sudo apt-get install inkscape

# install selenium
sudo apt-get install python-pip
sudo pip3.4 install selenium

# install geckodriver - firefox driver
wget https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz
tar xzvf geckodriver-v0.13.0-linux64.tar.gz 
sudo cp geckodriver /usr/bin/

# update firefox to latest
sudo apt-get update
sudo apt-get install firefox

