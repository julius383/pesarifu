# Pesarifu App

## Installing

- Clone repo
- `cd` into repo directory
    - run `poetry install`
    - run `npm install`
- cd into `reports/`
    - run `npm install`

Ensure the following vars are defined in the environment

- `MAIL_USER` - email used to send report to user.
- `MAIL_PASS` - password for the above email
- `CELERY_BROKER_URL` - url for celery broker, expects Redis
- `CELERY_RESULTS_BACKEND` - url for celery results backend, expects Redis can
  be same as `CELERY_BROKER_URL`
- `DB_URL` - url for accessing DB through SQLAlchemy, expects postgres
- `DEV_DB_URL` - alternate DB url for testing purposes
- `PROD` if set controls whether to use `DB_URL` or `DEV_DB_URL`
- `LOG_LEVEL` - default log level to use


## Running

- Make sure `redis` and `postgres` are started
- Use `just celery-run` to start celery workers
- Use `just website-serve` to start the web app
- Use `just reports-serve` to start the evidence report backend
