# raspi3--e-paper-display

**NOTE**: THIS README DESCRIBES THE DESIRED END STATE, BUT THE AUTOMATION IS STILL IN PROGRESS.

Display various information on an e-Paper display such as the one sold by Waveshare
[here](https://www.waveshare.com/product/7.5inch-hd-e-paper-b.htm). The connectivity is pretty
straightforward and utilizes a Raspberry Pi Zero WH and a HAT for the e-Paper controller.
Specifically, the following information is displayed and configurable via the
`config/settings.yml` file:

* RSS feed latest article details
* Day/date
* Stock symbol ticker (from Yahoo financials)
* Weather (current and current day forecast from OpenWeatherMap)
* Pi-Hole Ad-Blocking Statistics
* Last updated date/time

## Pi Hardware Configuration

The e-Paper display relies on the SPI interface to be enabled. Launch the Raspberry Pi configuration
utility and enable the SPI option, then reboot your Pi instance:

```bash
$ sudo raspi-config
# In the menu, navigate and select:
#    Interfacing Options -> SPI -> Yes
# then select Yes to reboot or perform the following:
$ sudo reboot
```

## Prerequisites

There are a few types of prerequisites needed in order for this service to function - specifically,
they are related to querying data sources and generating images, and the output of the image to the
e-paper display.

For common prerequisites, perform the following to set up your environment:

```bash
$ sudo apt-get -y install python3 python3-pip
$ pip3 install virtualenv
```

Next, clone the repository and create your virtual environment for configuration:

```bash
$ git clone https://github.com/jekhokie/electronicsbox.git
$ cd electronicsbox/raspi3--e-paper-display/
$ python3 -m virtualenv .env
$ . .env/bin/activate
```

### Data Sources and Display Prerequisites

Functionality in this script requires a specific font (Verdana), which is not
installed by default on the Raspbian OS. To install this font, run the following:

```bash
$ sudo apt-get -y install ttf-mscorefonts-installer
```

Next, install some other OS dependencies required by the service, including e-paper display
components needed to interact with the e-paper display:

```bash
$ sudo apt-get -y install libopenjp2-7 \
                          libtiff5 \
                          libatlas-base-dev \
                          python3-lxml
```

### E-Paper Display Prerequisites

The e-paper display also requires some additional work to make functional. Perform the following
to install BCM libraries, likely best from your home directory:

```bash
$ cd ~
$ wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
$ tar zxvf bcm2835-1.60.tar.gz
$ cd bcm2835-1.60/
$ sudo ./configure
$ sudo make
$ sudo make check
$ sudo make install
```

Next, wiringpi needs to be installed:

```bash
$ cd ~
$ sudo apt-get install wiringpi
$ wget https://project-downloads.drogon.net/wiringpi-latest.deb
$ sudo dpkg -i wiringpi-latest.deb
$ gpio -v
```

## Installation

Navigate back to the project directory and install your python dependencies and create your
environment-specific configuration file:

```
$ cd ~/electronicsbox/raspi3--e-paper-display/

# just in case you've lost the scope for python
$ . .env/bin/activate

$ pip install -r requirements.txt
$ cp config/settings.yml.sample config/settings.yml
$ vim config/settings.yml
# edit configurations to match your environment

$ chmod 600 config/settings.yml
# secure permissions since this file contains API keys
```

## Usage

Now that everything is installed, go ahead and run the script and you should see the e-Paper
display update after some time of gathering the various pieces of information that are needed
to populate the screen:

```bash
$ python main.py
```

## Improvements

To auto-load the functionality on boot of the Raspberry Pi, edit the file `/etc/rc.local` and
add the following right before the `exit 0` directive:

```bash
$ sudo vim /etc/rc.local
# add the following before `exit 0`:
#   ...
#   . /home/pi/electronicsbox/raspi3--e-paper-display/.env/bin/activate
#   python3 /home/pi/electronicsbox/raspi3--e-paper-display/main.py
#   exit 0
```

After doing this, reboot the Pi and your screen should auto-update at the set interval automatically
without you needing to log into the device and start the script.

## Credit

Some inspiration was taken from the following articles/posts:

- [7.5 Inch e-Paper HAT](https://www.waveshare.com/wiki/7.5inch_HD_e-Paper_HAT_(B))
- [e_paper_weather_display](https://github.com/AbnormalDistributions/e_paper_weather_display)
- [e-Paper Demo](https://github.com/waveshare/e-Paper)
