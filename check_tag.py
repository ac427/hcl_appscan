#!/bin/env python3
""" Script to verify if there is a version bump. """
import sys
import os
from shlex import split
import subprocess

if os.environ['TRAVIS_PULL_REQUEST'] == 'false':
    pass
else:
    def version_compare(master_version, new_version):
        """ Checks if new version is gt old. """
        if master_version == new_version:
            sys.exit("please bump the version!")
        arr1 = master_version.split('.')
        arr2 = new_version.split('.')
        # Initializer for the version arrays
        i = 0
        while i < len(arr1):
            # Version 2 is greater than version 1
            if arr2[i] > arr1[i]:
                print("new version looks good")
                sys.exit(0)
            # Version 1 is greater than version 2
            if arr1[i] > arr2[i]:
                sys.exit("please bump the version!")
            # We can't conclude till now
            i += 1

    VERSION_FILE = open("version", "r")
    NEW_VERSION = VERSION_FILE.read().strip('\n').split('=')[1]
    VERSION_FILE.close()

    MASTER_VERSION_CMD = "git show origin/master:version"
    CMD = split(MASTER_VERSION_CMD)
    OLD_VERSION = subprocess.Popen(CMD, stdout=subprocess.PIPE).communicate()[
        0].decode("utf-8").strip('\n').split('=')[1]

    version_compare(OLD_VERSION, NEW_VERSION)
