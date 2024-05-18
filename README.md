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

### Setup

- clone and `cd` into repo
- set your own values for the variables in `.env.example` and load it into the
  environment `source .env.example`
- ensure the following are defined in `pesarifu.config` folder
    - In `settings.toml`
        - `CELERY_BROKER_URL` - URL for celery broker, expects Redis
        - `CELERY_RESULTS_BACKEND` - URL for celery results backend, expects Redis can
           be same as `CELERY_BROKER_URL`
        - `APP_BASE_URL` - base web URL that app is deployed
        - `STATEMENTS_BASE_DIR` - where financial statements are stored after
           upload
        - `EXPORTS_BASE_DIR` - where csv/excel etc exports are stored before being
           sent
    - In `.secrets.toml`
        - `MAIL_USER` - email used to send report to user.
        - `MAIL_PASSWORD` - password for the `MAIL_USER` email
        - `TELEGRAM_BOT_TOKEN` - token for Telegram notifications
        - `DB_URL` - production and development url for accessing DB through SQLAlchemy,
           expects postgres e.g `DB_URL = "postgresql+psycopg2://postgres:@localhost:5432/pesarifu"`
- run `poetry install`
- run `npm install`
- run alembic to setup the database `alembic upgrade head`
- cd into `reports/`
    - run `npm install`
- (optional) run `python -m pesarifu.db.seed` to seed the database with
  some example data for a report.

### Running

- Make sure `redis` and `postgres` are running
- Use `just celery-run` to start celery workers
- Use `just app-run` to start the web app
- Use `just reports-serve` to start the evidence report back-end


[1]: https://evidence.dev/
