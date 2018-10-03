#!/bin/bash

TARGET="${LC_COMMIT_HASH:-origin/production}"
. .bashrc
APP_DIR=~/sahkopiikki
cd "$APP_DIR"

echo "# Starting deployment."
echo "# Target commit: ${TARGET}"
set -e # Fail the script on any errors.

nvm use 10
printf "# Node version: $(node --version)\n"
printf "# NPM version: $(npm --version)\n"

echo "# Stashing local changes to tracked files."
git stash

echo "# Fetching remote."
git fetch --all

echo "# Checking out the specified commit."
git checkout "${TARGET}"

echo "# Navigating to the backend directory."
cd backend

echo "# Activating virtualenv."
set +e # The activate script might return non-zero even on success
source ~/venv/bin/activate
set -e

echo "# Installing pip requirements."
pip install -r requirements.txt

echo "# Collecting static files."
python manage.py collectstatic --noinput

echo "# Taking a database backup."
mkdir -p backups
cp db.sqlite3 backups/db.sqlite3.bak_`date "+%Y-%m-%d"`

echo "# Running database migrations."
python manage.py migrate --noinput

echo "# Restarting the backend service."
sudo systemctl restart sahkopiikki

echo "# Navigating to the frontend directory."
cd ../frontend

echo "# Installing Node.js dependencies."
npm ci

echo "# Building the frontend project."
npx react-scripts build

echo "# Setting new build as the active build."
rm -rf "$APP_DIR/frontend/dist"
mv "$APP_DIR/frontend/build" "$APP_DIR/frontend/dist"

set +e
echo "# Deployment done!"