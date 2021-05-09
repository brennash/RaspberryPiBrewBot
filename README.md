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
database called brewbot. 

```
create database brewbot;
grant all privileges on brewbot.* to 'brewbot'@'localhost' IDENTIFIED BY 'brewpassword';
flush privileges;
```


## References
The AdaFruit LCD display API can be found here - https://circuitpython.readthedocs.io/projects/charlcd/en/latest/api.html
