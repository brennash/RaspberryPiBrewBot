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

	def addMeasurement(self, temperature):
		self.connect()
		self.cur = self.conn.cursor()
		self.cur.execute("INSERT INTO measurements (profile,date,temperature) VALUES (?, NOW(), ?)", (profile, temperature))
		self.conn.commit()
		self.conn.close()

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

