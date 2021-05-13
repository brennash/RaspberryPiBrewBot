import os
import sys
import time
import board
import busio
import random
from gpiozero import LED
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
from optparse import OptionParser


class PinOutputTest:

	def __init__(self, verboseFlag):
		self.verbose     = verboseFlag
		self.sleepTime   = 3
		lcd_columns      = 16
		lcd_rows         = 2
		i2c              = busio.I2C(board.SCL, board.SDA)
		self.lcd         = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

		# This might be the third from the right
		#self.led         = LED(14)
		self.led = LED(20)

	def run(self):
		counter = 0
		while counter < 60:
			self.lcd.clear()
			self.lcd.message = "ON "
			self.led.on()
			time.sleep(1)
			self.lcd.clear()
			self.lcd.message = "OFF"
			self.led.off()
			time.sleep(1)
			counter += 1

def main(argv):
	parser = OptionParser(usage="Usage: PinOutputTest.py [-v|--verbose]")
	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="Verbose logging")

	(options, filename) = parser.parse_args()

	pinIO = PinOutputTest(options.verboseFlag)
	pinIO.run()

if __name__ == "__main__":
	sys.exit(main(sys.argv))


