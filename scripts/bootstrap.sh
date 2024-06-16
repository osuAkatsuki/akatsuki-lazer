#!/usr/bin/env bash
set -eo pipefail

if [ -z "$APP_ENV" ]; then
  echo "Please set APP_ENV"
  exit 1
fi

if [[ $PULL_SECRETS_FROM_VAULT -eq 1 ]]; then
  akatsuki vault get akatsuki-lazer $APP_ENV -o .env
  source .env
fi

cd /srv/root

# run the service
exec /scripts/run-service.sh
