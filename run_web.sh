#!/bin/bash

source .venv/bin/activate

uvicorn app.main:app --host 127.0.0.1 --port 63591 --reload