#!/usr/bin/env python3

from flask import Flask, request, Response
import json
import phabricator

app = Flask(__name__)

with open('config.json') as f:
    conf = json.load(f)

phab = phabricator.Phabricator(conf['PHAB_HOST'], conf['PHAB_USER'], conf['PHAB_CERT'])

whitelisted = ['project.query', 'maniphest.info']

@app.route('/')
def home():
    return Response("""
fab-proxy allows unathenticated requests to Phabricator's API.

The following actions are allowed: %s.

Use /request/{method} and the parameters should be POSTed as a JSON object in the 'data' parameter.
    """.strip() % ', '.join(whitelisted), content_type='text/plain')


@app.route('/request/<action>')
def query(action):
    if action not in whitelisted:
        return json.dumps({'error': 'The %s action is not whitelisted' % action})

    params = request.form.get('data')
    if not params:
        return json.dumps({'error': 'No form data provided.'})
    data = phab.request(action, json.loads(params))
    return json.dumps(data)

if __name__ == '__main__':
    app.run()
