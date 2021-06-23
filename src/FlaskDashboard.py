import re
import io
import os
import csv
import datetime
import hashlib
import logging
from flask import session
from functools import wraps
from flask import render_template
from flask import Flask, request, Response
from logging.handlers import RotatingFileHandler
from flask import make_response, send_from_directory, redirect, url_for

# Call the flask application
app = Flask(__name__)

# Setup the app, with a random secret key for the sessions
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.secret_key = os.urandom(24).encode('hex')

# The main index page
@app.route('/')
def index():
	# Get the request IP Address
	reqIPAddr = request.remote_addr

	# Log the requestor details to file
	app.logger.info('User Request to index.html: {0}'.format(reqIPAddr))
	app.logger.info('Request URL: {0}'.format(request.url))
	app.logger.info('User Platform: {0}'.format(request.user_agent.platform))
	app.logger.info('User Browser: {0}'.format(request.user_agent.browser))
	app.logger.info('User Agent Version: {0}'.format(request.user_agent.version))
	app.logger.info('User Agent Language: {0}'.format(request.user_agent.language))
	app.logger.info('User Agent String: {0}'.format(request.user_agent.string))
	return render_template('index.html')

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

# The main calling class, running off port 1592
if __name__ == '__main__':
	handler = RotatingFileHandler('logs/dashboard.log', maxBytes=50000, backupCount=3)
	format = "%(asctime)s %(levelname)-8s %(message)s"
	handler.setFormatter(logging.Formatter(format))
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)
	app.run(host='0.0.0.0', port=1798)
