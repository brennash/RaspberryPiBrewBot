import os
import sys
import time
import datetime
import yaml
import logging
from Database import Database
from TemperatureSensor import TemperatureSensor
from optparse import OptionParser

class BrewBot:

	def __init__(self, configFilename, verboseFlag=False):
		self.database = None
		self.display = None
		self.ambientSensor = None

		self.initDatabase(configFilename)
		self.initSensors(configFilename)
		#logging.config.fileConfig('conf/logging.conf')
		#logger = logging.getLogger('simpleExample')

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
		path = data[1]['ambient_sensor']['path']
		hexId = data[1]['ambient_sensor']['hexId']
		filename = data[1]['ambient_sensor']['filename']
		self.ambientSensor = TemperatureSensor(path, hexId, filename)


	def run(self):

		while True:
			tempC, tempF = self.ambientSensor.getReading()
			print("{0}, Temp:{1}".format(datetime.datetime.now(), tempC))
			time.sleep(30)


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
			self.logger.info('Starting logging..')
		except Exception as err:
			errorStr = 'Error initializing log file, ',err
			print(errorStr)
			exit(1)


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


