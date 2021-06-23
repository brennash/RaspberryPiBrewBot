import os
import sys
import time
import board
import busio
import random
from gpiozero import LED
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from optparse import OptionParser


class LcdScreen:

	def __init__(self):
		lcd_columns      = 16
		lcd_rows         = 2
		i2c              = busio.I2C(board.SCL, board.SDA)
		self.lcd         = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
		self.ambient     = None
		self.fermenter   = None

	def updateAmbientTemp(self, temp):
		if temp is not None:
			self.ambient = temp

	def updateFermenterTemp(self, temp):
		if temp is not None:
			self.fermenter = temp

	def updateDisplay(self):
		lcdString = "Ambient: "
		if self.ambient is not None:
			lcdString += str(self.ambient)[0:4] + chr(223) + "C"
		lcdString += "\nSensor:  "
		if self.fermenter is not None:
			lcdString += str(self.fermenter)[0:4] + chr(223) + "C"
		self.lcd.clear()
		self.lcd.message = lcdString
