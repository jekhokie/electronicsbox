#!/usr/bin/env bash

# install dependencies
export CC=/usr/bin/gcc
sudo apt-get -y install python-dev libcairo2-dev libffi-dev build-essential apache2 libapache2-mod-wsgi

# install the service-identity module
sudo pip install service-identity threadpool pyasn1-modules python-memcached

# create the graphite group and user if they do not exist
g_group_exists=$(getent group _graphite >/dev/null 2>&1; echo $?)
if [ $g_group_exists != 0 ]; then
  sudo groupadd _graphite
fi

g_user_exists=$(id -u _graphite >/dev/null 2>&1; echo $?)
if [ $g_user_exists != 0 ]; then
  sudo useradd -c "Graphite User" -g _graphite -s /dev/null _graphite
fi

# perform install of whisper, carbon, and graphite-web if not yet installed
export PYTHONPATH="/opt/graphite/lib:/opt/graphite/webapp/"
if [ ! -d /opt/graphite/storage/whisper ]; then
  sudo pip install --no-binary=:all: https://github.com/graphite-project/whisper/tarball/master
fi

if [ ! -d /opt/graphite/lib/carbon ]; then
  sudo pip install --no-binary=:all: https://github.com/graphite-project/carbon/tarball/master
fi

if [ ! -d /opt/graphite/webapp ]; then
  sudo pip install --no-binary=:all: https://github.com/graphite-project/graphite-web/tarball/master
fi

# update configuration files to expected configs - note this is destructive
# and does not take into account local settings changed from what is checked
# into this repository
sudo cp configs/carbon.conf /opt/graphite/conf/carbon.conf
sudo cp configs/storage-schemas.conf /opt/graphite/conf/storage-schemas.conf
sudo cp configs/graphite.wsgi /opt/graphite/conf/graphite.wsgi

# copy local settings, but configure secret key (so it's not checked into source control)
local_settings=/opt/graphite/webapp/graphite/local_settings.py
sudo cp configs/local_settings.py $local_settings
scrt=$(grep SECRET_KEY ${local_settings} | awk -F' = ' '{print $2}')
if [ $scrt == "'UNSAFE_DEFAULT'" ]; then
  new_secret=$(date +%s | sha256sum | base64 | head -c 32; echo)
  sudo sed -i "s/SECRET_KEY = 'UNSAFE_DEFAULT'/SECRET_KEY = '${new_secret}'/" $local_settings
fi

# run migration for database storage
sudo PYTHONPATH=/opt/graphite/webapp django-admin.py migrate --noinput --settings=graphite.settings --run-syncdb

# copy static files for graphite-webapp if they don't already exist
if [ ! -d /opt/graphite/static ]; then
  sudo PYTHONPATH=/opt/graphite/webapp django-admin.py collectstatic --settings=graphite.settings --noinput
fi

# configure directories and permissions
sudo chown www-data:www-data /opt/graphite/storage/graphite.db
sudo mkdir -p /opt/graphite/storage/log/carbon-cache
sudo mkdir -p /opt/graphite/storage/log/carbon-relay
sudo mkdir -p /opt/graphite/storage/log/carbon-aggregator
sudo chown -R _graphite:_graphite /opt/graphite/storage/log
sudo chmod 775 /opt/graphite/storage
sudo chown -R _graphite /opt/graphite/storage/whisper
sudo chown www-data:_graphite /opt/graphite/storage
sudo chown www-data:_graphite /opt/graphite/conf/graphite.wsgi
sudo chown -R www-data /opt/graphite/storage/log/webapp
sudo chown -R www-data:_graphite /opt/graphite/static

# create Apache virtual host for Graphite Web
if [ ! -f /etc/apache2/sites-available/graphite-webapp.conf ]; then
  sudo cp configs/graphite-webapp.conf /etc/apache2/sites-available/graphite-webapp.conf
fi

# disable default site, enable graphite-webapp
needs_reload=0
if [ -L /etc/apache2/sites-enabled/000-default.conf ]; then
  sudo a2dissite 000-default
  needs_reload=1
fi

if [ ! -L /etc/apache2/sites-enabled/graphite-webapp.conf ]; then
  sudo a2ensite graphite-webapp
  needs_reload=1
fi

# perform Apache reload to align enabled/disabled sites
if [ $needs_reload == 1 ]; then
  sudo systemctl reload apache2
fi

# copy a service script for use
if [ ! -f /etc/init.d/carbon-cache ]; then
  sudo cp configs/carbon-cache /etc/init.d/carbon-cache
  sudo chmod 755 /etc/init.d/carbon-cache
  sudo update-rc.d carbon-cache defaults
fi

# start carbon cache if not already running
cc_running=$(sudo service carbon-cache status >/dev/null 2>&1; echo $?)
if [ $cc_running != 0 ]; then
  sudo service carbon-cache start
fi

echo "------------------------------------------------------------"
echo "All Set!"
echo "Some interesting things you can do:"
echo "1. Send test data to Graphite from localhost:"
echo "     echo \"test.something.foo 2 \`date +%s\`\" | nc -w1 localhost 2003"
echo "   Then, investigate the metric:"
echo "     /usr/local/bin/whisper-fetch.py /opt/graphite/storage/whisper/test/something/foo.wsp"
echo "2. Visit the graphite-webapp web application:"
echo "     http://localhost/"
echo "------------------------------------------------------------"
