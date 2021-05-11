import re
import sys
import yaml
import json
import logging
import unittest
import datetime
from Database import Database

class Test(unittest.TestCase):

	def setUp(self):
		with open('conf/config_test.yaml', "r") as yamlfile:
			data = yaml.load(yamlfile, Loader=yaml.FullLoader)
		username = data[0]['database']['username']
		password = data[0]['database']['password']
		database = data[0]['database']['database']
		hostname = data[0]['database']['hostname']
		port     = data[0]['database']['port']
		self.database = Database(hostname, port, username, password, database)

	def test_(self):
		self.assertTrue(True)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
