#!/bin/bash
# No more than 100 lines of code

populate_env_variables() {
  set -o allexport
  [[ -f /src/gtranslate/.env ]] && source /src/gtranslate/.env
  set +o allexport
  echo "env variables are populated"
}

dev() {
  python app.py
}

populate_env_variables
dev
