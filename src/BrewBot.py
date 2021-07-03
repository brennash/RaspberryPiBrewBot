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
		self.profileId = None

		# Setup Logging
		self.logger = None
		self.logFile = os.environ['HOME'] + '/RaspberryPiBrewBot/logs/brewbot.log'
		self.setupLogging()

		# Initialize the database, temp sensor and display
		self.initDatabase(configFilename)
		self.initSensors(configFilename)
		self.initDisplay()

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
		try:
			with open(filename, "r") as yamlfile:
				data = yaml.load(yamlfile, Loader=yaml.FullLoader)
			username = data[0]['database']['username']
			password = data[0]['database']['password']
			database = data[0]['database']['database']
			hostname = data[0]['database']['hostname']
			port     = data[0]['database']['port']
			self.database = Database(hostname, port, username, password, database)

			# Get the brew profile for this brewing
			self.profileId = data[3]['brew_profile']['id']

		except Exception as err:
			self.logger.error("Error initializing Database - {0}".format(err))

	def initSensors(self, filename):
		try:
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
		except Exception as err:
			self.logger.error("Error initializing Sensor - {0}".format(err))


	def initDisplay(self):
		self.display = LcdScreen()
		self.display.updateDisplay()

	def run(self):
		sensorTempC, sensorTempF = self.probeSensor.getReading()

		minTemp = float(self.database.getMinTemp(self.profileId)[0])
		maxTemp = float(self.database.getMaxTemp(self.profileId)[0])

		self.display.updateFermenterTemp(sensorTempC)
		self.display.updateDisplay()

		if minTemp <= sensorTempC and sensorTempC <= maxTemp:
			tempRange = True
			self.logger.info("Temp {0} C, within bounds {1} to {2}".format(sensorTempC, minTemp, maxTemp))
		else:
			tempRange = False
			self.logger.info("Temp {0} C, outside of bounds {1} to {2}".format(sensorTempC, minTemp, maxTemp))

		self.database.addMeasurement(self.profileId, sensorTempC, tempRange)

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


