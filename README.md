# Pesarifu

Pesarifu is an application for conducting data analysis of
financial statements, primarily from mobile transactions. Current
features include:

- Data Extraction from PDF Statements into SQL Tables. Supports PDFs from
    - [x] Safaricom (MPesa)
    - [ ] Standard Chartered
    - [ ] Equity
- Export transactions to CSV, JSON and Excel files.
- Report generation using [Evidence][1]

See `examples/mpesa.pdf` for an example statement and
`examples/'Financial Report by Pesarifu for John Mwangi.pdf'` for an example
output report produced by the application.

Additional documentation can be found in `docs/`.


## Usage

### Installing

- Clone repo
- `cd` into repo directory
    - run `poetry install`
    - run `npm install`
- cd into `reports/`
    - run `npm install`

Ensure the following variables are defined in the environment

- `ENV_FOR_DYNACONF` - controls which section to load settings from in
`src/pesarifu/config/settings.toml`, `development` or `production`
- `APP_ROOT` - root directory of project on your system
- `ROOT_PATH_FOR_DYNACONF` - where to find dynaconf settings files


Ensure the following are defined in `pesarifu.config` folder

- In `settings.toml`
    - `MAIL_USER` - email used to send report to user.
    - `CELERY_BROKER_URL` - URL for celery broker, expects Redis
    - `CELERY_RESULTS_BACKEND` - URL for celery results backend, expects Redis can
       be same as `CELERY_BROKER_URL`
    - `APP_BASE_URL` - base web URL that app is deployed
    - `STATEMENTS_BASE_DIR` - where financial statements are stored after
       upload
    - `EXPORTS_BASE_DIR` - where csv/excel etc exports are stored before being
       sent
- In .secrets.toml
    - `MAIL_PASSWORD` - password for the `MAIL_USER` email
    - `TELEGRAM_BOT_TOKEN` - token for Telegram messaging
    - `DB_URL` - production and development url for accessing DB through SQLAlchemy, expects postgres


### Running

- Make sure `redis` and `postgres` are running
- Use `just celery-run` to start celery workers
- Use `just website-serve` to start the web app
- Use `just reports-serve` to start the evidence report back-end



[1]: https://evidence.dev/
