#!/bin/sh
uvicorn "app.api:app" --host $SERVER_HOST --port $SERVER_PORT --reload 
exec "$@"