#!/usr/bin/env python3

import os
import sys
import adal
import json
from flask import Flask
import requests

if  'AUTHORITY' and \
    'RESOURCE' and \
    'USERNAME' and \
    'PASSWORD' and \
    'CLIENTID' not in os.environ:
        print("""
            Error:
              You are missing one or more
              environment variables.
              See README.
            """, file=sys.stderr)
        sys.exit(1)

app = Flask(__name__, static_url_path='/static')

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/api/token')
def get_token():
    context = adal.AuthenticationContext(
        os.environ['AUTHORITY'],
        validate_authority=True,
        api_version=None)

    token_response = context.acquire_token_with_username_password(
        os.environ['RESOURCE'],
        os.environ['USERNAME'],
        os.environ['PASSWORD'],
        os.environ['CLIENTID']
)
    aad_token = token_response['accessToken']

    headers = {'Authorization': 'Bearer ' + aad_token}
    response = requests.get(
        'https://api.powerbi.com/v1.0/myorg/groups', headers=headers)

    bi_groups = json.loads(response.text)['value']
    group_id = bi_groups[0]['id']

    response = requests.get(
        'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports', headers=headers)

    bi_reports = json.loads(response.text)['value']
    report_id = bi_reports[2]['id']
    embed_url = bi_reports[2]['embedUrl']

    post_data = post_data = \
    """
        {
            "accessLevel": "View"
        }
    """

    headers.update({'Content-type': 'application/json'})

    response = requests.post('https://api.powerbi.com/v1.0/myorg/groups/' + group_id + \
         '/reports/' + report_id + '/GenerateToken',data = post_data, headers=headers)

    report_token = json.loads(response.text)['token']

    j = '{{\
            "embedToken": "{:s}",\
            "embed_url": "{:s}",\
            "report_id": "{:s}"\
         }}'.format(report_token, embed_url, report_id)

    return j, 200, {'Content-Type': 'application/json'}

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)