#!/bin/env python3
""" Runs asoc static scan. """
import os
import subprocess
import json
from shlex import split
import requests


def scan(pr_data):
    """ Runs static scan on download src. """
    key_id = os.environ['KEY_ID']
    key_secret = os.environ['KEY_SECRET']
    app_id = ''
    build_id = str(pr_data[3])

    def appscan_auth():
        """ Auth to appscan."""
        headers = {
            'Content-Type ': 'application/json',
            'Accept': 'application/json'}

        data = {
            "KeyId": "{}".format(key_id),
            "KeySecret": "{}".format(key_secret)}
        return requests.post(
            'https://cloud.appscan.com/api/V2/Account/ApiKeyLogin',
            headers=headers, data=data)

    def appscan_cli_auth():
        """ CLI authentication to cloud. """
        cli_auth_cmd = [
            'appscan.sh',
            'api_login',
            '-P',
            key_secret,
            '-u',
            key_id,
            '-persist']
        print("Doing CLI a auth ....")
        subprocess.Popen(
            cli_auth_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()

    scan_cmd = ['appscan.sh', 'prepare', '-n', build_id]
    print("Starting scan ....")
    scan_out = subprocess.Popen(
        scan_cmd,
        cwd=build_id,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT).communicate()
    print(scan_out)

    response = appscan_auth()
    token = response.json()['Token']
    headers = {'Accept': 'application/json',
               "Authorization": "Bearer {}".format(token)}
    url = 'https://cloud.appscan.com/api/V2/Apps?api_key=' + token
    response = requests.get(url,
                            headers=headers)
    for app in response.json():
        if app['Name'] == pr_data[0]:
            app_id = (app['Id'])

    project_data = split(
        "find ./" +
        build_id +
        " -maxdepth 2 -name asoc_project.json")
    data_path = subprocess.check_output(project_data).decode("utf-8").strip()
    data = open(data_path, 'rb')
    payload = json.loads(data.read())
    data.close()

    if not app_id:
        response = requests.post(
            url,
            headers=headers, data=payload)
        app_id = response.json()['Id']
    appscan_cli_auth()
    upload_irx_cmd = split(
        "appscan.sh queue_analysis -a " +
        app_id +
        " -f " +
        build_id +
        "/" +
        build_id +
        ".irx -n " + build_id)

    print("Starting upload of irx  ....")
    upload_irx = subprocess.check_output(
        upload_irx_cmd).decode("utf-8").strip()
    print(upload_irx)
