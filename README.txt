# install python 3.4
sudo apt-get install python3.4
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3.4 get-pip.py
sudo pip3.4 install beautifulsoup4
sudo pip3.4 install lxml

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

