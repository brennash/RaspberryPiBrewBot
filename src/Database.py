import sys
import mariadb

class Database:

	def __init__(self, hostname, port, username, password, database):
		self.hostname = hostname
		self.port = port
		self.username = username
		self.password = password
		self.database = database

		self.conn = None
		self.cur = None

	def truncateMeasurements(self):
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("TRUNCATE measurements")
		self.conn.commit()
		self.conn.close()

	def addMeasurement(self, profile_id, fermenter_temp, within_temp_range):
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("INSERT INTO measurements (profile_id, measurement_date, fermenter_temp, within_temp_range) VALUES (?, NOW(), ?, ?)", (profile_id, fermenter_temp, within_temp_range))
		self.conn.commit()
		self.conn.close()

	def getMinTemp(self, profile_id):
		result = None
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT min_temp FROM brew_profile WHERE profile_id=?", (profile_id,))
		for min_temp in self.cur:
			result = min_temp
		self.conn.close()
		return result

	def getMaxTemp(self, profile_id):
		result = None
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT max_temp FROM brew_profile WHERE profile_id=?", (profile_id,))
		for max_temp in self.cur:
			result = max_temp
		self.conn.close()
		return result

	def getCurrentDbTime(self):
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("SELECT NOW() AS datetime")
		for datetime in self.cur:
			print(f"{datetime}")
		self.conn.commit()
		self.conn.close()

	def connect(self):
		try:
			self.conn = mariadb.connect(
			user=self.username,
			password=self.password,
			host=self.hostname,
			port=self.port,
			database=self.database)
		except mariadb.Error as e:
			print("Error connecting to MariaDB Platform: {e}")
			sys.exit(1)

