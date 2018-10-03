#!/bin/bash
. .bashrc
APP_DIR=~/sahkopiikki
cd "$APP_DIR"

echo "# Starting deployment."
set -e # Fail the script on any errors.

echo "# Stashing local changes to tracked files."
git stash

echo "# Fetching remote."
git fetch --all

echo "# Checking out production."
git checkout production

echo "# Pulling latest changes."
git pull

echo "# Navigating to the frontend directory."
cd frontend

echo "# Installing Node.js dependencies."
npm ci

echo "# Building the frontend project."
set +e # The build script might return non-zero even on success
npm run build
set -e

echo "# Setting new build as the active build."
rm -rf "$APP_DIR/frontend/dist"
mv "$APP_DIR/frontend/build" "$APP_DIR/frontend/dist"

echo "# Navigating to the backend directory."
cd ../backend

echo "# Activating virtualenv."
set +e # The activate script might return non-zero even on success
source ~/venv/bin/activate
set -e

echo "# Installing pip requirements."
pip install -r requirements.txt

echo "# Collecting static files."
python manage.py collectstatic

echo "# Taking a database backup."
mkdir -p backups
cp db.sqlite3 backups/db.sqlite3.bak_`date "+%Y-%m-%d"`

echo "# Running database migrations."
python manage.py migrate

echo "# Restarting the backend service."
sudo systemctl restart sahkopiikki

set +e
echo "# Deployment done!"