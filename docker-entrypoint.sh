#!/bin/bash
set -e

PORT=${2:-8000}

case "$1" in
    init)
        yoyo apply migrations/
        ;;
    api)
        exec uvicorn src.app:app --host 0.0.0.0 --port $PORT --forwarded-allow-ips '*'
        ;;
    start)
        yoyo apply migrations/
        uvicorn src.app:app --host 0.0.0.0 --port $PORT --reload
        ;;

    *)
        exec "$@"
        ;;
esac
