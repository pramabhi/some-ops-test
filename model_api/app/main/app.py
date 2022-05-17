import os
import pickle
import logging
import ast
import jwt
import json
import pandas as pd
import numpy as np
from flask import Flask, request, _request_ctx_stack, g
from flask_restplus import Api, Resource, fields
from flask_track_usage import TrackUsage
from flask_track_usage.storage.printer import PrintWriter
from flask_track_usage.storage.output import OutputWriter
from flask_script import Manager
from functools import wraps
from healthcheck import HealthCheck
from slackclient import SlackClient
from typing import Dict
from werkzeug.contrib.fixers import ProxyFix

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

slack_client = SlackClient(SLACK_TOKEN)
model = tf.keras.models.load_model('/model/yolo_model')

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

def predict_result(last_sixty_seconds_of_prices):
    return model.predict(last_sixty_seconds_of_prices)

app = Flask(__name__)
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'include'

health = HealthCheck()

@app.route('/predict', methods=['POST'])
@token_required
def predict():
    last_sixty_seconds = request.get('data')
    return jsonify(prediction=predict_result(last_sixty_seconds))

t = TrackUsage(app, [
		PrintWriter(),
		OutputWriter(transform=lambda s: "OUTPUT: " + str(s))
	])
@t.include
@app.route('/')
def index():
	g.track_var["optional"] = "Write_Something"
	return "Hello"

def download_model():
    # Copy model from cloud bucket

with app.app_context():
    download_model()

app.add_url_rule("/health-check", "healthcheck", view_func=lambda: health.run())

@manager.command
def run():
    app.run(host='0.0.0.0', port='5000')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()

