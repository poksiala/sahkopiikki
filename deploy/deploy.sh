chmod 600 deploy/deploy_key;
cat deploy/update_app.sh | ssh -oStrictHostKeyChecking=no -i deploy/deploy_key "$DEPLOY_USER@$DEPLOY_SERVER"
