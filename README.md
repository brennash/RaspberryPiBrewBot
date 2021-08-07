# RaspberryPiBrewBot
A temperature controller for DIY beer fermenter. 

## Setup


## Brewing How-To Guide
For brevity, there's a quick [how-to guide to brewing](docs/BREWING.md) that will go through the various steps getting setup to brew. 

## Materials
The following list of materials are required to build out this temperature controller. 

* [Waterproof Temperature Sensor](https://store.brewpi.com/waterproof-onewire-temperature-sensor-rj11-ds18b20)
* [Ambient Temperature Sensor](https://ie.rs-online.com/web/p/temperature-humidity-sensor-ics/1901709/) 
* [RJ12 Sockets](https://ie.rs-online.com/web/p/development-tool-accessories/1683093/)
* [LCD Shield with buttons](https://thepihut.com/products/adafruit-blue-white-16x2-lcd-keypad-kit-for-raspberry-pi)
* [Raspberry Pi 3 Model B+](https://thepihut.com/products/raspberry-pi-3-model-b-plus)
* [NOOBS Pre-installed Micro SD Card](https://thepihut.com/products/noobs-preinstalled-sd-card)
* [Raspberry Pi 3 Power Supply](https://thepihut.com/products/official-raspberry-pi-universal-power-supply)
* [PHAT Stack Breakout Board](https://ie.farnell.com/pimoroni/pim322/phat-stack-fully-assembled/dp/3446772)



### Setting up the 1-Wire Bus
The temperature sensors use the GPIO-4 pin on the Raspberry Pi, and can be used in a bus setup, i.e.,
multiple temperature sensors can use the same wire. However, to enable it, you need to edit the 
```/boot/config.txt``` file and add the following line, 

```
dtoverlay=w1-gpio,gpiopin=4
```

When you are wiring up the [DS18B20 probe](https://store.brewpi.com/waterproof-onewire-temperature-sensor-rj11-ds18b20), 
using the [RJ12 socket](https://ie.rs-online.com/web/p/development-tool-accessories/1683093/) 
you need to wire the following, 

* GPIO4 pin into PGC
* GND pin into PGD
* 3.3V pin into GND

Restart the Raspberry Pi and then do an ```lsmod``` that hopefully shows up the following, 

```
lsmod | grep w1

w1_therm               20480  0
w1_gpio                16384  0
wire                   36864  2 w1_gpio,w1_therm
```

Or you can prompt the Pi to look for newly connected devices using, 

```
sudo modprobe w1-gpio
```

Once it's working the sensor will start writing to a file in ```/sys/bus/w1/devices/<some-hex-number>/w1_slave```. The 
HEX number is a unique address of the sensor, in my case I see the following, 

```
ls /sys/bus/w1/devices/
28-0000087faf90  28-00000d19dabd  w1_bus_master1
```

You can view the ```w1_slave``` in each of those ```28-00000xxxxxx``` folders and you'll see something like below to know it's working. 

```
6b 01 4b 46 7f ff 05 10 49 : crc=49 YES
6b 01 4b 46 7f ff 05 10 49 t=22687
```

The first line has a ```YES``` to indicate the temperature measurement is valid, the end of the 
second line ```t=22687``` indicates the temperature in thousands of a degree Celsius, so in this 
instance it's showing a rather balmy 22.687 degrees C. 

### Setting up the LCD
The I/O to communicate with the LCD shield needs to be enabled in the Raspberry Pi config settings, 
so first, go into the ```raspi-config``` and under Interface Options set the appropriate I2C flag. 

Next you need to install the Python library to support the LCD.
```
sudo pip3 install adafruit-circuitpython-charlcd
```

## Database
I've installed and tested lots of databases on lots of systems, but this is my first attempt at a DB on 
a Raspberry Pi, so the recommendatations seem to be to use the MariaDB as it's slightly better at caching
and a bit less taxing on the I/O to the MicroSD card. 

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install mariadb-server
sudo mysql_secure_installation
```

Then setup a database and a user to your liking. For simplicity here, we've a user called brewbot and a 
database called brewbot (and another called brewbot_test). 

Access the root user CLI using

```
sudo mysql
```

Then run the following commands to create the brewbot and brewbot_test databases.


```
create database brewbot;
create database brewbot_test;
grant all privileges on brewbot.* to 'brewbot'@'localhost' IDENTIFIED BY 'brewbot';
grant all privileges on brewbot_test.* to 'brewbot'@'localhost' IDENTIFIED BY 'brewbot';
flush privileges;
```

Once you've created the user (brewbot) and the DB (brewbot) then just run this script to create the necessary tables

```
mysql -u brewbot -D brewbot -p < sql/build_tables.sql 
mysql -u brewbot -D brewbot_test -p < sql/build_test_tables.sql 
```

## Setting up the Config
```yaml
- database:
    hostname: localhost
    port: 3306
    username: brewbot
    password: mypassword
    database: brewbot
```

## Running the Brewbot Code
Once you've everything setup, the next step is to enable the code to start running once your Raspberry Pi is powered on. 
Since you've got an LCD display, the first boot screen should show the temperature reading and the IP address of the Pi. 

### Starting the code at boot time
We want to have the code start execution immediately when the Raspberry Pi finishes booting up. Even when there may be power outages 
to the Pi, we want it to come back up and continue taking sensor readings. The easiest way to do this is using the crontab file. 

First create a run script that will get called periodically, so that it runs the python script using the appropriate configuration 
settings. In this example, we've created a file in ```/home/pi/runScript.sh``` with the following details.

```
#!/bin/bash
python3 /home/pi/RaspberryPiBrewBot/src/BrewBot.py /home/pi/RaspberryPiBrewBot/conf/my_brew_config.yaml
```

Adjust the above paths to point at where you've installed the brewbot and the config, and then set the file so that it's executable by 
the crontab, e.g., 

```
chmod 755 /home/pi/runScript.sh
```

Once you've done that you need to insert the command to run this script at a set interval. This is done by adding your file to the crontab schedule 
as follows, 

```
crontab -e
```

The above command will let you configure how regularly the BrewBot will take sensor readings and commit them to the 
database. Typically, a 5 minute interval is sufficient, since it will let the heating or cooling element take effect. Enter the following line, 

```
*/5 * * * * /home/pi/runScript.sh
```

## Charting
The graphical temperature chart is done using [Chart.min.js](https://cdnjs.com/libraries/Chart.js) with [Python Flask](https://flask.palletsprojects.com/en/2.0.x/) 
providing the underlying framework. 

## References

| Reference | URL |
| --- | --- |
| The AdaFruit LCD display API | https://circuitpython.readthedocs.io/projects/charlcd/en/latest/api.html |
| The Raspberry Pi LCD Wiring Guide | https://learn.adafruit.com/character-lcds/python-circuitpython#python-and-circuitpython-usage-7-12 |
| Setting up scripts to boot up straight | https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/init-script |
| I2C Pinout Schematic | https://pinout.xyz/pinout/i2c |
| GPIO code sample | https://www.raspberrypi.org/documentation/usage/gpio/python/README.md |
| LCD Pinout Schematic | https://learn.adafruit.com/assets/938 | 
| DS18B20 Wiring Diagram | http://www.d3noob.org/2018/04/this-post-is-part-of-book-raspberry-pi_24.html |
| Reading temperatures using a DS18B20 | https://raspbrew.tumblr.com/post/39850791984/reading-temperatures-on-a-raspberry-pi-using | 
| DS18B20 Wiring Setup | https://www.mkompf.com/weather/pionewiremini.html | 
| Python Process Supervisor | http://supervisord.org/running.html#adding-a-program |
