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
		self.databaseDb = Database(hostname, port, username, password, database)

	def test_MinTemp_1(self):
		minTemp = self.databaseDb.getMinTemp(1)
		self.assertIsNotNone(minTemp)

	def test_MinTemp_2(self):
		minTemp = self.databaseDb.getMinTemp(1)
		self.assertEquals(minTemp[0], 20.0)

	def test_MaxTemp_1(self):
		maxTemp = self.databaseDb.getMaxTemp(1)
		self.assertEquals(maxTemp[0], 25.0)

	def test_getMeasurements_1(self):
		self.databaseDb.truncateMeasurements()
		self.databaseDb.addMeasurement(1, 21.0, True)
		self.databaseDb.addMeasurement(1, 22.0, True)
		labels, temps, range = self.databaseDb.getMeasurements(1)
		self.assertIsNotNone(results)

	def test_getMeasurements_1(self):
		self.databaseDb.truncateMeasurements()
		self.databaseDb.addMeasurement(1, 21.0, True)
		self.databaseDb.addMeasurement(1, 22.0, True)
		labels, temps, range = self.databaseDb.getMeasurements(1)
		self.assertIsNotNone(range)

	def test_getMeasurements_2(self):
		self.databaseDb.truncateMeasurements()
		self.databaseDb.addMeasurement(1, 21.0, True)
		self.databaseDb.addMeasurement(1, 22.0, True)
		result = True
		labels, temps, range = self.databaseDb.getMeasurements(1)
		todayStr = datetime.datetime.now().strftime('%Y%m%d')
		for row in labels:
			testStr = row.strftime('%Y%m%d')
			if testStr != todayStr:
				result = False
		self.assertTrue(result)

	def test_getMeasurements_3(self):
		self.databaseDb.truncateMeasurements()
		self.databaseDb.addMeasurement(1, 21.0, True)
		self.databaseDb.addMeasurement(1, 22.0, True)
		self.databaseDb.addMeasurement(1, 23.0, True)
		labels, temps, range = self.databaseDb.getMeasurements(1)
		self.assertTrue(len(temps) == 3)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
