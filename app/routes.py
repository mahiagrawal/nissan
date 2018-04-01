#! /usr/bin/python

from app import app
from flask import render_template, redirect, url_for, request, Flask
from flask_mqtt import Mqtt
import ast 
import sqlquery

topic = ''
coordinates = {}

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'User'}
    posts = [
        {
            'car': {'model': 'GTR'},
            'Status': 'Up and Running fine'
        },
        {
            'car': {'model': 'Pathfinder'},
            'Status': 'Up and Running fine'
        },
        {
            'car': {'model': 'Juke'},
            'Status': 'Up and Running fine'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	user = request.form['username']
    	passw = request.form['password']

    	count = sqlquery.check_credentials(user, passw)[0][0]
    	if(count!=0):
    		global topic
        	topic = sqlquery.get_topic(user,passw)[0][0]
        else:
            error = 'Invalid Credentials. Please try again.'
    if(topic != ''):
		return redirect(url_for('mapbox'))
    else:	
    	return render_template('login.html', error=error)

@app.route('/mapbox')
def mapbox():
	mqtt  = Mqtt(app)
	@mqtt.on_connect()
	def handle_connect(client, userdata, flags, rc):
		if(topic=='all'):
			mqtt.subscribe('owntracks/nwgmhdaf/#')
		else:
			mqtt.subscribe(topic)
	@mqtt.on_message()
	def handle_mqtt_message(client, userdata, message):
		data = dict(
			topic=message.topic.encode('ascii', 'ignore'),
			payload=message.payload.encode('ascii', 'ignore')
		)
		d = ast.literal_eval(data['payload'])
		global coordinates
		coordinates[data['topic']] = [d['lon'], d['lat']]
	return redirect(url_for('mapmake')) 

@app.route('/mapmake')
def mapmake():
	points = [j for v in coordinates.values() for j in v]
	return render_template('mapbox_js.html', points=points, topics=coordinates.keys())