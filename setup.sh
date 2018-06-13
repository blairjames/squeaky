#!/bin/bash
echo 'Squeaky uses Python 3, please ensure it is installed locally.'
echo 'Please run this script with root permissions'
cd /opt
/bin/git clone https://github.com/blairjames/squeaky.git
chmod -R 755 squeaky
sleep 1
