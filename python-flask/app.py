#!/usr/bin/env python3

import os
import sys
import adal
import json
from flask import Flask, render_template
import requests
import conf
import logging

log = logging.getLogger(__file__)

# Read environment variables from the config file
# if it is not set
if  'AUTHORITY' and \
    'RESOURCE' and \
    'USERNAME' and \
    'PASSWORD' and \
    'CLIENTID' and \
    'BACKEND_URL' not in os.environ:
        conf.setenv()

log.debug("Env vars: \n" + str(os.environ))

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

    # If PBI_WORKSPACE_NAME is set, get workspace with that name
    # If it is not set or no such workspace, get the first workspace
    bi_groups = json.loads(response.text)['value']
    log.debug("group info:\n" + str(bi_groups))

    group_id = ""
    if "PBI_WORKSPACE_NAME" in os.environ:
        for gid in bi_groups:
            if gid['name'] == os.environ["PBI_WORKSPACE_NAME"]:
                group_id = gid['id']

    if group_id == "":
        log.warn("Workspace name is set but there is no such workspace: " + os.environ["PBI_WORKSPACE_NAME"])
        group_id = bi_groups[0]['id']

    response = requests.get(
        'https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports', headers=headers)

    # Pick the 1st report in the App Workspace (aka group)
    bi_reports = json.loads(response.text)['value']

    log.debug("Reports json:\n"+ str(bi_reports))

    report_id = embed_url = ""
    if "PBI_REPORT_NAME" in os.environ:
        for rid in bi_reports:
            if rid['name'] == os.environ["PBI_REPORT_NAME"]:
                report_id = rid['id']
                embed_url = rid['embedUrl']

    if report_id == "":
        log.warn("Report name is set but there is no such report: " + os.environ["PBI_REPORT_NAME"])
        report_id = bi_reports[0]['id']
        embed_url = bi_reports[0]['embedUrl']

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
    return render_template('index.html', backend_url = os.environ['BACKEND_URL'])

if __name__ == '__main__':
    log.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL",logging.WARNING)))
    #log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(stream = sys.stdout))

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)