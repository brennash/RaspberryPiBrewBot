import os
import sys
import time
import board
import busio
import random
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from optparse import OptionParser


class Thermometer:

	def __init__(self, verboseFlag):
		self.verbose     = verboseFlag
		self.sleepTime   = 0.2
		lcd_columns      = 16
		lcd_rows         = 2
		i2c              = busio.I2C(board.SCL, board.SDA)
		self.lcd         = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

		# Create the degree symbol at character \x01
		self.lcd.create_char(1,[12,18,18,12,0,0,0,0])

		# Create the X and Tick symbols at \x02 and \x03 respectively
		self.lcd.create_char(2,[0,27,14,4,14,27,0,0])
		self.lcd.create_char(3,[0,1,3,22,28,8,0,0])

		# Create the Thermometer symbol at \x04
		self.lcd.create_char(4,[4,10,10,10,17,31,14,0])
		self.lcd.clear()

		# The upper and lower temperature bounds
		self.minTargetTemp = 20.0
		self.maxTargetTemp = 22.0

	def run(self):
		while True:
			currentTemp = self.getCurrentTemp()
			self.displayTempScreen(currentTemp)
			time.sleep(self.sleepTime)

	def getCurrentTemp(self):
		return random.uniform(18.0, 35.0)

	def displayTempScreen(self, currentTemp):
		if self.minTargetTemp <= currentTemp and currentTemp <= self.maxTargetTemp:
			inRange = True
		else:
			inRange = False
		self.lcd.message = self.getTempDisplayMessage(currentTemp, inRange)


	def getTempDisplayMessage(self, temp, inRange=False):
		tempStr = '{0:.1f}'.format(temp)

		if len(tempStr) < 4:
			lcdDisplay = "Temp  "+tempStr+"\x01C"
		else:
			lcdDisplay = "Temp "+tempStr+"\x01C"

		if inRange == False:
			lcdDisplay += "  \x04 \x02\n"
		else:
			lcdDisplay += "  \x04 \x03\n"

		return lcdDisplay


	def getTemperature(self):
		temperature = random.uniform(20.0, 23.0)



def main(argv):
	parser = OptionParser(usage="Usage: Thermometer [-v|--verbose]")
	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="Verbose logging")

	(options, filename) = parser.parse_args()

	temp = Thermometer(options.verboseFlag)
	temp.run()

if __name__ == "__main__":
	sys.exit(main(sys.argv))


