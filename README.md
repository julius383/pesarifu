# Pesarifu App

## Installing

- Clone repo
- `cd` into repo directory
    - run `poetry install`
    - run `npm install`
- cd into `reports/`
    - run `npm install`

Ensure the following vars are defined in the environment

- `ENV_FOR_DYNACONF` - controls which environment to load settings from
  (`development` and `production`)
- `APP_ROOT` - root directory of project
- `ROOT_PATH_FOR_DYNACONF` - where to find dynaconf settings files


Ensure the following are defined in `pesarifu.config` folder

- In `settings.toml`
    - `MAIL_USER` - email used to send report to user.
    - `CELERY_BROKER_URL` - url for celery broker, expects Redis
    - `CELERY_RESULTS_BACKEND` - url for celery results backend, expects Redis can
       be same as `CELERY_BROKER_URL`
    - `LOG_LEVEL` - default log level to use
    - `APP_BASE_URL` - base web url that app is deployed
    - `STATEMENTS_BASE_DIR` - where financial statements are stored after
       upload
    - `EXPORTS_BASE_DIR` - where csv/excel etc exports are stored before being
       sent
- In .secrets.toml
    - `MAIL_PASS` - password for the `MAIL_USER` email
    - `DEV_DB_URL` - alternate DB url for testing purposes
    - `DB_URL` - url for accessing DB through SQLAlchemy, expects postgres


## Running

- Make sure `redis` and `postgres` are started
- Use `just celery-run` to start celery workers
- Use `just website-serve` to start the web app
- Use `just reports-serve` to start the evidence report backend
