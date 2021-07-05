import re
import io
import os
import csv
import yaml
import datetime
import hashlib
import logging
import binascii
from flask import session
from functools import wraps
from Database import Database
from flask import render_template
from flask import Flask, request, Response
from logging.handlers import RotatingFileHandler
from flask import make_response, send_from_directory, redirect, url_for

# Call the flask application
app = Flask(__name__)

# Setup the app, with a random secret key for the sessions
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.secret_key = binascii.hexlify(os.urandom(24))

# Setup the config file
app.config['CONFIG_FILE'] = 'conf/config.yaml'

# The database
databaseDb = None

# The main index page
@app.route('/')
def index():
	# Get the request IP Address
	reqIPAddr = request.remote_addr

	# Setup the database connection
	initDatabase(app.config['CONFIG_FILE'])

	# Log the requestor details to file
	app.logger.info('User Request to index.html: {0}'.format(reqIPAddr))
	app.logger.info('Request URL: {0}'.format(request.url))
	app.logger.info('User Platform: {0}'.format(request.user_agent.platform))
	app.logger.info('User Browser: {0}'.format(request.user_agent.browser))
	app.logger.info('User Agent Version: {0}'.format(request.user_agent.version))
	app.logger.info('User Agent Language: {0}'.format(request.user_agent.language))
	app.logger.info('User Agent String: {0}'.format(request.user_agent.string))

	if databaseDb is not None:
		labels24,  temps24,  range24 = databaseDb.getMeasurements(-24)
	else:
		app.logger.error("Database is not initialized")
		labels24 = []
		temps24  = []
		range24  = []
	#labels8,  temps8,  range8 = database.getMeasurements(-8)
	#labels24, temps24, range24 = database.getMeasurements(-24)

	return render_template('index.html', labels=labels24, values=temps24, legend="Previous 24 hours")

@app.route('/temp', methods=['GET','POST'])
def search():
	# Get the request IP Address
	reqIPAddr = request.remote_addr

	if request.method == 'POST':
		app.logger.info('Temp POST Request: {0}'.format(reqIPAddr))
		searchStr = request.form.get('search_text')
		return render_template('search.html', temp=temp)
	else:
		app.logger.warning('GET request to /temp endpoint: {0}'.format(reqIPAddr))
		return redirect(url_for('index'))


def initDatabase(filename):
	try:
		with open(filename, "r") as yamlfile:
			data = yaml.load(yamlfile, Loader=yaml.FullLoader)
		username   = data[0]['database']['username']
		password   = data[0]['database']['password']
		database   = data[0]['database']['database']
		hostname   = data[0]['database']['hostname']
		port       = data[0]['database']['port']
		databaseDb = Database(hostname, port, username, password, database)
		app.logger.info("Database successfully initialized")
	except Exception as err:
		app.logger.error('Error initializing database {0}'.format(err))


# The main calling class, running off port 1592
if __name__ == '__main__':
	handler = RotatingFileHandler('logs/dashboard.log', maxBytes=50000, backupCount=3)
	format = "%(asctime)s %(levelname)-8s %(message)s"
	handler.setFormatter(logging.Formatter(format))
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)
	app.run(host='0.0.0.0', port=1798)
