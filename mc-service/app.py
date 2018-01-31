# -*- coding: utf-8 -*-
"""Example Master Controller with a REST API and a Redis backing service."""

import redis
from flask import Flask, jsonify, request


# Create Flask application
APP = Flask(__name__)


STATES = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
          'UNKNOWN']


@APP.route('/state', methods=['GET'])
def get_state():
    """Return the SDP State."""
    state = 'UNKNOWN'
    try:
        data = redis.Redis(host='master_db')
        state = data.get('state')
        if state is None:
            data.set('state', 'INIT')
            state = 'INIT'
        else:
            state = state.decode('utf-8')
    except redis.exceptions.ConnectionError:
        return service_unavailable()
    return jsonify(state=state)

@APP.route('/state', methods=['PUT'])
def set_state():
    """Trigger state change"""
    request_data = request.get_json(silent=False)
    state = request_data['state']
    response = service_unavailable()
    if state.upper() not in STATES:
        response = jsonify(error='Invalid state.')
        response.status_code = 400
    else:
        try:
            data = redis.Redis(host='master_db')
            data.set('state', state)
            response = jsonify(message='Accepted state: ' + state)
        except redis.exceptions.ConnectionError:
            response = jsonify(message='Unable to process request')
            response.status_code = 404

    return response


@APP.errorhandler(404)
def not_found(error=None):
    """Example custom error handler"""
    response = jsonify(error='Invalid URL: ' + request.url)
    response.status_code = 404
    return response


@APP.errorhandler(503)
def service_unavailable(error=None):
    """Example custom error handler"""
    response = jsonify(error='Service Unavailable')
    response.status_code = 503
    return response

if __name__ == '__main__':
    APP.run(debug=True)
