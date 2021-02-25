# Portfolio projects api
##### A starter template for building rest apis with django

Make sure to look at the [pycharm config](ideaConfig.md)

## Development
### Requirements
You will need the following to run the app
- docker ([installation](https://docs.docker.com/get-docker/))
- docker-compose ([installation](https://docs.docker.com/compose/install/))

### Setup
Perform these steps to quickly get started

**Note:** ports 8000 and 5444 need to be available
```shell script
cd projects_api
docker-compose up -d
```

The api should be available at http://localhost:8000

You can always use the following command to stop execution:
```bash
docker-compose down
```

### Tests
Use this command to run tests:
```bash
docker-compose run api sh -c "python manage.py test"
```