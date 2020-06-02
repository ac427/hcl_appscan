#!/bin/env python3
""" Python script to listen to github pr payload. """
import os
import time
import urllib.request
import glob
from zipfile import ZipFile
from stat import S_IXUSR
import shutil
from download import download_src
from asoc_scan import scan
from bottle import run, post, request


@post('/pr')
def index():
    """ Listen to pull payload and run asoc scan. """
    post_action = ['synchronize', 'opened', 'reopened']
    post_data = dict(request.json)
    if post_data['action'] in post_action:
        pr_info = []
        pr_info.append(post_data['repository']['full_name'])
        # pr_info.append(post_data['number'])
        pr_info.append(post_data['pull_request']['head']['sha'])
        pr_info.append(post_data['installation']['id'])
        pr_info.append(int(time.time()))
        download_src(pr_info)
        scan(pr_info)
        # clean up
        shutil.rmtree(str(pr_info[3]))
        os.remove(str(pr_info[3]) + ".tar")
    else:
        pass


run(host='0.0.0.0', port=5000, debug=True)
