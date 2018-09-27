chmod 600 /tmp/deploy_key;
ssh -oStrictHostKeyChecking=no -i /tmp/deploy_key "$DEPLOY_USER@$DEPLOY_SERVER" 'zsh deploy_sahkopiikki.sh';
