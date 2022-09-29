#!/bin/sh

set -e

. /venv/bin/activate

exec uvicorn src.main:app --host 0.0.0.0 --port 80
