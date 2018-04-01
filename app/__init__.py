#! /usr/bin/python

from flask import Flask

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'm11.cloudmqtt.com'
app.config['MQTT_BROKER_PORT'] = 16221
app.config['MQTT_USERNAME'] = 'nwgmhdaf'
app.config['MQTT_PASSWORD'] = 'gRTeNQxde3_p'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds


from app import routes