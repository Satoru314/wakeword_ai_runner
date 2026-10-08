#!/usr/bin/env bash

uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt
