#!/bin/env python3
""" Downloads github repo as tarball. """

import os
import tarfile
import requests
import jwt
from cryptography.hazmat.backends import default_backend


def download_src(info):
    """ Download the src repo to scan. """
    pem_file = 'acbot.2020-05-29.private-key.pem'
    cert = open(pem_file, 'r')
    cert_bytes = cert.read().encode()
    private_key = default_backend().load_pem_private_key(cert_bytes, None)
    cert.close()

    def app_headers(epoch):
        payload = {
            # issued at time
            'iat': epoch,
            # expiration time
            'exp': epoch + (5 * 60),
            # GitHub App's identifier
            'iss': '523'
        }

        web_token = jwt.encode(payload, private_key, algorithm='RS256')

        headers = {"Authorization": "Bearer {}".format(web_token.decode()),
                   "Accept": "application/vnd.github.machine-man-preview+json"}
        return headers

    epoch_time = info[3]
    os.mkdir(str(epoch_time))
    response = requests.get(
        'https://github.ibm.com/api/v3/app',
        headers=app_headers(epoch_time))

    response = requests.post(
        'https://github.ibm.com/api/v3/installations/{}/access_tokens'.format(info[2]),
        headers=app_headers(epoch_time))
    token = response.json()['token']
    headers = {"Authorization": "token {}".format(token)}
    url = 'https://github.ibm.com/api/v3/repos/' + \
        info[0] + '/tarball/' + info[1]
    response = requests.get(url, headers=headers)

    download = requests.get(response.url, stream=True)
    if download.status_code == 200:
        with open(str(epoch_time) + '.tar', 'wb') as file:
            file.write(download.raw.read())
        tar = tarfile.open(str(epoch_time) + '.tar')
        tar.extractall(path=str(epoch_time))
        tar.close()
