#!/usr/bin/env bash

# create the apt repository
if [ ! -f /etc/apt/sources.list.d/grafana.list ]; then
  sudo cp configs/grafana.list /etc/apt/sources.list.d/grafana.list
  sudo apt-get update
fi

# add GPG keys
key_exist=$(sudo apt-key list | grep -i grafana >/dev/null 2>&1; echo $?)
if [ $key_exist != 0 ]; then
  curl https://packages.grafana.com/gpg.key | sudo apt-key add -
fi

# check if grafana package exists and if not, install it and configure to
# launch at boot time
graf_exist=$(sudo dpkg -l | grep -i grafana >/dev/null 2>&1; echo $?)
if [ $graf_exist != 0 ]; then
  sudo apt-get -y install grafana
  sudo update-rc.d grafana-server defaults
fi

# start the service
graf_running=$(sudo service grafana-server status >/dev/null 2>&1; echo $?)
if [ $graf_running != 0 ]; then
  sudo service grafana-server start
fi

echo "------------------------------------------------------------"
echo "All Set!"
echo "You should be able to visit the Grafana website/interface"
echo "by navigating to the following URL:"
echo "   http://localhost:3000/"
echo "The default login is admin/admin."
echo "------------------------------------------------------------"
