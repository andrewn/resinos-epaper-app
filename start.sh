#!/usr/bin/env bash

# echo "Starting app..."

# cd /epaper/gratis/PlatformWithOS/demo
# python DrawDemo.py

if [ -n "${TIMEZONE}" ]
then
  echo "Setting timezone ${TIMEZONE}"
  echo "${TIMEZONE}" > /etc/timezone && dpkg-reconfigure tzdata
fi

echo "Starting epd-fuse service"
service epd-fuse start

echo "Starting..."
cd /usr/src/app
python calendar.py
