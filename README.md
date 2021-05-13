# RaspberryPiBrewBot
A temperature controller for DIY beer fermenter. 

## Setup

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
mysql -u brewbot -D brewbot_test -p < sql/build_tables.sql 
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
We want to have the code start execution immediately when the Raspberry Pi finishes booting up. 


## References
The AdaFruit LCD display API can be found here - https://circuitpython.readthedocs.io/projects/charlcd/en/latest/api.html

The Raspberry Pi LCD Wiring Guide - https://learn.adafruit.com/character-lcds/python-circuitpython#python-and-circuitpython-usage-7-12

Setting up scripts to boot up straight away - https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/init-script
