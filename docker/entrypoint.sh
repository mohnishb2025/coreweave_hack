#!/bin/sh
set -eu

if [ "$#" -eq 0 ]; then
  set -- python -m pytest -q
fi

exec "$@"
