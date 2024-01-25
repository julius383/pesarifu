# Application Structure

Generate an update listing with `just overview`

```sh
.
├── doc                                    # project documentation
├── src
│  └── pesarifu
│  │  ├── api                              # definition for app.pesarifu.com
│  │  │  ├── __init__.py
│  │  │  ├── app.py
│  │  │  └── dependencies.py
│  │  ├── config
│  │  │  ├── celery.py
│  │  │  └── constants.py
│  │  ├── db                               # Data Model
│  │  │  ├── models.py
│  │  │  └── util.py
│  │  ├── etl
│  │  │  ├── safaricom                     # workflow definition for Safaricom
│  │  │  │  ├── __init__.py                # task entry point definition for provider
│  │  │  │  ├── extract.py                 # extract fields from supported sources e.g PDF and API JSON
│  │  │  │  ├── load.py                    # store and retrieve data from data store
│  │  │  │  ├── tasks.py                   # celery tasks definitions
│  │  │  │  └── transform.py               # process and enrich data after extract before load
│  │  │  ├── stanchart
│  │  │  └── __init__.py
│  │  ├── templates
│  │  │  ├── email-report.html.jinja       # template for report email
│  │  │  └── index.html                    # main page for app.pesarifu.com
│  │  └── util
│  │     ├── export.py                     # functions for exporting transactions to various formats
│  │     ├── helpers.py
│  │     ├── notify.py
│  │     └── tasks.py
│  ├── reports                             # analytical reports
│  │  ├── pages
│  │  │  └── pesarifu.md
│  │  ├── sources                          # definition for data stores available for use in reports
│  │  │  └── pesarifu
│  │  │     ├── accounts.sql
│  │  │     ├── connection.yaml
│  │  │     └── transactions.sql
│  │  ├── evidence.plugins.yaml
│  │  └── README.md
│  └── static                              # css for app.pesarifu.com/
│     └── src
│        └── input.css
├── justfile                               # project related tasks definition
├── pyproject.toml
├── README.md
└── tailwind.config.js

```
