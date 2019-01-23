# 17-graphite-tsdb-with-statsd-and-grafana

Since Raspberry Pi is exceptionally good with communication with sensors, it only makes sense we start
to design a data-logger by way of a time-series database. What better place to start than with the
beloved Graphite stack (Carbon, Graphite-Webapp, and Whisper). This will lay the groundwork for sprinkling
sensors all over the place and having them report into the Raspberry Pi instance for their respective data
points to be recorded and visualized. Additionally, we will be using statsd in front of Graphite in order to
avoid needing to send a specific time data point along with the measured data due to the fact that obtaining
time on an ESP8266-01 is extremely difficult due to there not being any internal clock (and requiring a direct
query to an NTP time server, which consumes time, adds complexity, and consumes more battery power).

Obviously there are many provisioning/automation techniques to install and configure software on a Linux-based
operating system, but for simplicity sake, I've chosen to write a couple of bash scripts to perform the
work which can eventually be translated into something such as Ansible.

## Description of Contents

First, a quick description of what exists in this tutorial:

- `configs/`: Directory containing the respective configurations used by the installers.
- `install_graphite.sh`: Script to install prerequisites and associated packages for the Graphite stack.
- `install_grafana.sh`: Script to install prerequisites and associated packages for Grafana.
- `install_statsd.sh`: Script to install prerequisites and associated packages for statsd.
- `README.md`: This README

## Installing Graphite (Carbon, Graphite-Webapp, Whisper)

First, we'll want to install the Graphite components. Running Raspbian 9 (Stretch) installing the tools is
as simple as running the following script, which will handle all prerequisites, install Graphite stack,
and enable your integrations. Note that at the time of this script development, Graphite 1.0.5 was
available and the version tested in this stack, so your mileage may vary if you veer from the respective
tested versions of OS and software:

```bash
$ ./install_graphite.sh
```

Once Graphite and its components have been installed, there are a couple of different things you can do (as
noted by the script output). First, you can visit the Graphite webapp front-end by navigating to the URL
`http://localhost/`. You should be able to browse the built-in 'carbon' metrics to visualize time-series
data that is being pumped in by the carbon agent.

Second, you can test ingesting data right away from the command line. Execute the following command:

```bash
$ echo "test.something.foo 2 `date +%s`" | nc -w1 localhost 2003
```

Upon running the above command, a new set of whisper files will be created with the naming convention
of the passed metric in `/opt/graphite/storage/whisper/test/something/foo.wsp`, where the filename is
the Whisper file for the metric. You can inspect this file by using the `whisper-fetch.py` script
like so:

```bash
$ /usr/local/bin/whisper-fetch.py /opt/graphite/storage/whisper/test/something/foo.wsp
```

You now have a fully-functioning Graphite setup for ingesting metrics from sensors that have the ability
to transmit packets over the same network that the Raspberry Pi is running the Graphite stack!

## Installing Grafana

Now that we have a fully-functioning Graphite instance we can put the spectacular Grafana web interface
in front if it for visualizations. At the time of this project, Grafana version 5.4.3 was being used
along with Raspbian 9 (Stretch) - same disclaimer applies for variation in versions. Simply run the
following script to get the Grafana interface installed:

```bash
$ ./install_grafana.sh
```

Once Grafana has been installed, you can log into the interface using the default login credentials
`admin/admin` by visiting the following URL: `http://localhost:3000`.

Once logged in, add a Graphite data source by pointing the source to `http://localhost` and testing the
connection. If all goes well, you're off to the races and can start visualizing the data coming into the
Graphite stack running on the same Raspberry Pi.

## Installing Statsd

The last component is to install the statsd application. This enables us to avoid needing to send a time
stamp to the collecting server, which is helpful due to the lack of time management on the ESP8266.
Simply run the following script to get statsd installed:

```bash
$ ./install_statsd.sh
```

Just like the original Graphite installation, you can manually send a data point to the statsd interface
which will pass the data to the Graphite back-end. Execute the following command:

```bash
$ echo "test.something.foo:5|g" | nc -u -w1 localhost 8125
```

Upon running the above command, a new set of whisper files will be created with the naming convention
of the passed metric in `/opt/graphite/storage/whisper/test/something/foo.wsp`, where the filename is
the Whisper file for the metric. You can inspect this file by using the `whisper-fetch.py` script
like so:

```bash
$ /usr/local/bin/whisper-fetch.py /opt/graphite/storage/whisper/stats/gauges/test/something/foo.wsp
```
