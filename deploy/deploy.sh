#!/bin/bash
# Change permissions to something that SSH accepts
chmod 600 deploy/deploy_key;

# Pipe the update script over SSH to the production server
cat deploy/update_app.sh | ssh -oStrictHostKeyChecking=no -i deploy/deploy_key "$DEPLOY_USER@$DEPLOY_SERVER"
