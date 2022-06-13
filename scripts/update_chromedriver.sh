#!/bin/bash

rm ./temp/chromedriver.zip
rm ./bin/chromedriver

LATEST_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE);
wget -O ./temp/chromedriver.zip https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip;
unzip ./temp/chromedriver.zip -d ./bin

rm ./temp/chromedriver.zip

echo "Starting main application again"

/bin/bash ./start.sh