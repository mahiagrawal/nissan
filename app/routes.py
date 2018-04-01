#! /usr/bin/python

from app import app
from flask import render_template, redirect, url_for, Flask, request
from flask_mqtt import Mqtt
import ast 
import sqlquery
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

topic = ''
coordinates = {}

mqtt = Mqtt(app)
socketio = SocketIO(app)

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
    global topic
    if request.method == 'POST':
    	user = request.form['username']
    	passw = request.form['password']

    	count = sqlquery.check_credentials(user, passw)[0][0]
    	if(count!=0):
        	topic = sqlquery.get_topic(user,passw)[0][0]
        else:
            error = 'Invalid Credentials. Please try again.'
    if(topic != ''):
        return redirect(url_for('mapbox'))
    else:	
    	return render_template('login.html', error=error)

@app.route('/mapbox')
def mapbox():
    global topic
    return render_template('mapbox_js.html', topic = topic)

@socketio.on('subscribe')
def handle_subscribe(message):
    if(message=='all'):
        mqtt.subscribe('owntracks/nwgmhdaf/#')
    else:
        mqtt.subscribe(message)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic.encode('ascii', 'ignore'),
        payload=message.payload.encode('ascii', 'ignore')
    )
    d = ast.literal_eval(data['payload'])
    global coordinates
    coordinates[data['topic']] = [d['lon'], d['lat']]
    points = coordinates.values()
    socketio.emit('mqtt_message', data=points)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, use_reloader=True, debug=True)
