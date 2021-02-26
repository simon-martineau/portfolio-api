# Portfolio projects api
A rest api for portfolio projects build with [django rest framework](https://github.com/encode/django-rest-framework)

## Development
Make sure to look at the [pycharm config](ideaConfig.md) for django integrations.
### Requirements
The following installations are required:
- docker ([installation](https://docs.docker.com/get-docker/))
- docker-compose ([installation](https://docs.docker.com/compose/install/))

### Setup
Perform these steps to quickly get started

**Note:** ports 8000 and 5444 must be available. Port 5444 is open so it is possible to query the contained database from the host. It can be removed safely.
```shell script
cd projects_api
docker-compose up -d
```

The api should be available at http://localhost:8000

### Tests
Use this command to run tests:
```bash
docker-compose run api sh -c "python manage.py test"
```

### Deploy
For deployment, look at the [deploy notes](deploy.md)
