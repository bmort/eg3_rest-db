# -*- coding: utf-8 -*-
"""Example Master Controller with a REST API and a Redis backing service."""

import os

import redis
from flask_api import FlaskAPI, status
from flask import request


APP = FlaskAPI(__name__)
DB = redis.Redis(host=os.getenv('DATABASE_HOST'))


@APP.route('/state', methods=['GET', 'PUT'])
def state():
    """Return the SDP State."""
    states = ['OFF', 'INIT', 'STANDBY', 'ON', 'DISABLE', 'FAULT', 'ALARM',
              'UNKNOWN']

    if request.method == 'PUT':
        requested_state = request.data.get('state', '').upper()
        if requested_state not in states:
            return ({'error': 'Invalid state: {}'.format(requested_state),
                     "allowed_states": states},
                    status.HTTP_400_BAD_REQUEST)
        DB.set('state', requested_state)
        return {'message': 'Accepted state: {}'.format(requested_state)}

    current_state = DB.get('state')
    if current_state is None:
        DB.set('state', 'INIT')
        current_state = 'INIT'
    else:
        current_state = current_state.decode('utf-8')
    return {'state': current_state}
