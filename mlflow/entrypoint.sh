#!/bin/sh
mlflow server \
--backend-store-uri postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB \
--default-artifact-root $ARTIFACT_STORE \
--host $SERVER_HOST \
--port $SERVER_PORT
exec "$@"
