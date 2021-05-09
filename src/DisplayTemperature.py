import os
import sys
import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from optparse import OptionParser


class DisplayTemperature:

	def __init__(self, verboseFlag):
		self.verbose     = verboseFlag
		self.sleepTime   = 0.1
		lcd_columns      = 16
		lcd_rows         = 2
		i2c              = busio.I2C(board.SCL, board.SDA)
		self.lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
		self.lcd.clear()

	def run(self):
		while True:
			if self.lcd.down_button:
				self.lcd.message = "Down"
			elif self.lcd.left_button:
				self.lcd.message = "Left"
			else:
				self.lcd.message = "Python"
			time.sleep(self.sleepTime)

def main(argv):
	parser = OptionParser(usage="Usage: DisplayTemperature [-v|--verbose]")
	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="Verbose logging")

	(options, filename) = parser.parse_args()

	temp = DisplayTemperature(options.verboseFlag)
	temp.run()

if __name__ == "__main__":
	sys.exit(main(sys.argv))


