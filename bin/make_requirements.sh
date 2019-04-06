#!/usr/bin/env bash
.venv/bin/pip-compile
.venv/bin/pip install -r requirements.txt
yarn install
./node_modules/.bin/gulp vendor
