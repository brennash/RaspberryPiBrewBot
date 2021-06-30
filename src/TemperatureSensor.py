import os
import glob
import time

class TemperatureSensor:

	def __init__(self, path, hexId, filename):
		self.deviceFile = path + '/' + hexId + '/' + filename

	def readFromFile(self):
		try:
			file = open(self.deviceFile, 'r')
			lines = file.readlines()
			file.close()
			return lines
		except Exception as error:
			return None

	def getReading(self):
		lines = self.readFromFile()
		if lines is None:
			return None, None
		else:
			if len(lines) != 2:
				return None, None

			if lines[0].strip()[-3:] != 'YES':
				return None, None

			index = lines[1].find('t=')
			tempStr = lines[1][index+2:]
			tempC   = float(tempStr) / 1000.0
			tempF   = ((tempC * 9.0) / 5.0) + 32.0
			return tempC, tempF
