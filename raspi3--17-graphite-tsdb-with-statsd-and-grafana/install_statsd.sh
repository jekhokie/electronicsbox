#!/usr/bin/env bash

# install dependencies
sudo apt-get -y install nodejs

# clone the repository if not yet in place
if [ ! -d /opt/statsd ]; then
  sudo git clone https://github.com/etsy/statsd.git /opt/statsd
fi

# copy the respective configuration file - note that this is destructive and
# does not take into account local settings changes from what is checked into
# this repository
sudo cp configs/statsdConfig.js /opt/statsd/

# create the logs directory if it doesn't already exist
if [ ! -d /opt/statsd/logs ]; then
  sudo mkdir /opt/statsd/logs
  sudo chmod 777 /opt/statsd/logs
fi

# start statsd
nohup node /opt/statsd/stats.js /opt/statsd/statsdConfig.js 2>&1 >/opt/statsd/logs/statsd.log &

echo "------------------------------------------------------------"
echo "All Set!"
echo "Some interesting things you can do:"
echo "1. Send test data to statsd from localhost:"
echo "     echo \"test.something.foo:5|g\" | nc -u -w1 localhost 8125"
echo "   Then, investigate the metric:"
echo "     /usr/local/bin/whisper-fetch.py /opt/graphite/storage/whisper/test/something/foo.wsp"
echo "------------------------------------------------------------"
