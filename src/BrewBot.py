import os
import sys
import yaml
from Database import Database
from optparse import OptionParser

class BrewBot:

	def __init__(self, configFilename, verboseFlag=False):
		self.database = None
		self.display = None

		self.initDatabase(configFilename)
		self.database.getCurrentDbTime()

	def initDatabase(self, filename):
		with open(filename, "r") as yamlfile:
			data = yaml.load(yamlfile, Loader=yaml.FullLoader)
		username = data[0]['database']['username']
		password = data[0]['database']['password']
		database = data[0]['database']['database']
		hostname = data[0]['database']['hostname']
		port     = data[0]['database']['port']
		self.database = Database(hostname, port, username, password, database)



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


