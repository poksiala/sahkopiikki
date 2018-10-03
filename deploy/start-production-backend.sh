#!/bin/bash

# Find out the location of the script, not the working directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# Navigate to the backend directory
cd "${DIR}/../backend"

# Activate virtualenv
. ~/venv/bin/activate

# Start Django with Gunicorn
gunicorn -w 4 --access-logfile - --error-logfile - sahkopiikki.wsgi
