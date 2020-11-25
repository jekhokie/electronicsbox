# raspi3--e-paper-display

**NOTE**: THIS README DESCRIBES THE DESIRED END STATE, BUT THE AUTOMATION IS STILL IN PROGRESS.

Display various information on an e-Paper display such as the one sold by Waveshare
[here](https://www.waveshare.com/product/7.5inch-hd-e-paper-b.htm). The connectivity is pretty
straightforward and utilizes a Raspberry Pi Zero WH and a HAT for the e-Paper controller.
Specifically, the following information is displayed and configurable via the
`config/settings.yml` file:

* RSS feed latest article details
* Day/date
* Stock symbol ticker
* Weather (current and current day forecast)
* Sonos "What's playing"
* Last updated date/time

## Prerequisites

This script requires Python 3 on your Raspberry Pi in order to function - first, install this
version of Python and pip if they do not already exist, as well as virtualenv:

```bash
$ sudo apt-get -y install python3 python3-pip
$ pip3 install virtualenv
```

In addition, the functionality in this script requires a specific font (Verdana), which is not
installed by default on the Raspbian OS. To install this font, run the following:

```bash
$ sudo apt-get -y install ttf-mscorefonts-installer
```

## Installation

Next, clone the repository to your Raspbery Pi and create a configuration file with
your desired settings:

```
$ cp config/settings.yml.sample config/settings.yml
$ vim config/settings.yml
# edit configurations to match your environment

$ chmod 600 config/settings.yml
# secure permissions since this file contains API keys
```

Once you have a configuration file in place, initialize your virtual environment and install
the dependent libraries:

```bash
$ python3 -m virtualenv .env
$ . .env/bin/activate
$ pip install -r requirements.txt
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
#   . /home/pi/raspi3--e-paper-display/.env/bin/activate
#   python3 /home/pi/raspi3--e-paper-display/main.py
#   exit 0
```

After doing this, reboot the Pi and your screen should auto-update at the set interval automatically
without you needing to log into the device and start the script.

## Credit

Some inspiration was taken from the following articles/posts:

- [e_paper_weather_display](https://github.com/AbnormalDistributions/e_paper_weather_display)
