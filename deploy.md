# Deploy notes
## Environement variables
Make sure to set all necessary environment variables in instance/production.env

## Dokku
Here are the steps to deploy using dokku

See https://dokku.com/docs/getting-started/installation/ for installing dokku
#### On the dokku host
These commands need to be executed on the dokku host
```shell script
sudo dokku apps:create projects-api
sudo dokku plugins:install https://github.com/dokku/dokku-postgres.git postgres
sudo dokku postgres:create drs-database
sudo dokku postgres:link drs-database projects-api
```

Also, point your app to the environment variables file:
```shell script
sudo dokku config:set projects-api ENV_PATH=instance/production.env
```

Also, set your domains for the app like this: (and don't forget to point your dns records to the dokku host,
at least for the active apps)
```shell script
dokku domains:add projects-api api.simonmartineau.dev
```

#### On the git repo
All we need is to add the remote and push a subtree:
```shell script
git remote add dokku dokku@<server_ip>:projects-api
git push dokku master
```

#### SSL with letsencrypt
Once your app is up and running, you need to enable https with the following
```shell script
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
sudo dokku config:set --no-restart projects-api DOKKU_LETSENCRYPT_EMAIL=your@email.tld
sudo dokku letsencrypt projects-api
```

And you're done!