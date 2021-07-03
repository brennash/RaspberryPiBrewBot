import os
import sys
import time
import datetime
import yaml
import logging
from logging.handlers import RotatingFileHandler
from Database import Database
from LcdScreen import LcdScreen
from TemperatureSensor import TemperatureSensor
from optparse import OptionParser

class BrewBot:

	def __init__(self, configFilename, verboseFlag=False):
		self.database = None
		self.display = None
		self.ambientSensor = None
		self.probeSensor = None

		self.initDatabase(configFilename)
		self.initSensors(configFilename)
		self.initDisplay()

		self.logger = None
		self.logFile = 'logs/brewbot.log'
		self.setupLogging()


	def setupLogging(self):
		""" 
		Sets up the logging function to write data to the log folder with a rotating file logger.
		"""
		try:
			self.logger = logging.getLogger(__name__)
			handler = RotatingFileHandler(self.logFile, maxBytes=500000, backupCount=5)
			format  = "%(asctime)s %(levelname)-8s %(message)s"
			handler.setFormatter(logging.Formatter(format))
			handler.setLevel(logging.INFO)
			self.logger.addHandler(handler)
			self.logger.setLevel(logging.INFO)
		except Exception as err:
			errorStr = 'Error initializing log file, ',err
			print(errorStr)
			exit(1)

	def initDatabase(self, filename):
		with open(filename, "r") as yamlfile:
			data = yaml.load(yamlfile, Loader=yaml.FullLoader)
		username = data[0]['database']['username']
		password = data[0]['database']['password']
		database = data[0]['database']['database']
		hostname = data[0]['database']['hostname']
		port     = data[0]['database']['port']
		self.database = Database(hostname, port, username, password, database)

	def initSensors(self, filename):
		with open(filename, "r") as yamlfile:
			data = yaml.load(yamlfile, Loader=yaml.FullLoader)
		ambPath     = data[1]['ambient_sensor']['path']
		ambHexId    = data[1]['ambient_sensor']['hexId']
		ambFilename = data[1]['ambient_sensor']['filename']

		prbPath     = data[2]['probe_sensor']['path']
		prbHexId    = data[2]['probe_sensor']['hexId']
		prbFilename = data[2]['probe_sensor']['filename']

		self.ambientSensor = TemperatureSensor(ambPath, ambHexId, ambFilename)
		self.probeSensor   = TemperatureSensor(prbPath, prbHexId, prbFilename)

	def initDisplay(self):
		self.display = LcdScreen()
		self.display.updateDisplay()

	def run(self):
		#tempC, tempF             = self.ambientSensor.getReading()
		sensorTempC, sensorTempF = self.probeSensor.getReading()
		self.display.updateFermenterTemp(sensorTempC)
		self.display.updateDisplay()
		if 20.0 >= sensorTempC and sensorTempC <= 24:
			tempRange = True
		else:
			tempRange = False

		self.logger.info("Temp {0} C".format(sensorTempC))

		self.database.addMeasurement("Starter", sensorTempC, tempRange, 9.99, False, False)

def main(argv):
	parser = OptionParser(usage="Usage: BrewBot [-v|--verbose] <config-file>")
	parser.add_option("-v", "--verbose",
		action="store_true",
		dest="verboseFlag",
		default=False,
		help="Verbose logging")

	(options, filename) = parser.parse_args()

	if len(filename) == 0:
		parser.print_help()
		sys.exit(1)
	else:
		brewbot = BrewBot(filename[0], options.verboseFlag)
		brewbot.run()

if __name__ == "__main__":
	sys.exit(main(sys.argv))


