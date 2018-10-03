#!/bin/bash
. .bashrc
nvm use 10
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
npm run build

echo "# Setting new build as the active build."
rm -rf "$APP_DIR/frontend/dist"
mv "$APP_DIR/frontend/build" "$APP_DIR/frontend/dist"

echo "# Navigating to the backend directory."
cd ../backend

echo "# Activating virtualenv."
set +e # The activate script might return non-zero even on success
source venv/bin/activate
set -e

echo "# Installing pip requirements."
pip install -r requirements.txt

echo "# Restarting the backend service."
sudo systemctl restart sahkopiikki

set +e
echo "# Deployment done!"