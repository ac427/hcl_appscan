#!/bin/env python3
""" Pushed the content in version file as github tag.
    run the script on merge. """
import os
import github

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO_NAME = os.environ['TRAVIS_REPO_SLUG']

G = github.Github(
    base_url="https://api.github.com",
    login_or_token=GITHUB_TOKEN)

REPO = G.get_repo(REPO_NAME)

SHA = REPO.get_commit('master').sha


VERSION_FILE = open("version", "r")
VERSION = VERSION_FILE.read().strip('\n').split('=')[1]
VERSION_FILE.close()

TAGGER = github.InputGitAuthor('bot', 'bot@localhost')

REPO.create_git_tag(VERSION, 'auto push tag' + VERSION, SHA, 'commit', TAGGER)

REPO.create_git_ref("refs/tags/v" + VERSION, SHA)
