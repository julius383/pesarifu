# Application Structure

Generate an updated listing with `just overview`

```sh
.
├── alembic                                 # database migration
│  ├── versions
│  │  ├── 6e6e9fc78065_initial_migration.py
│  │  └── e7a3b53426f3_create_contact_request_table.py
│  ├── env.py
│  └── script.py.mako
├── docs
│  ├── adding-financial-providers.md
│  ├── app-structure.md
│  ├── architecture.png
│  ├── database.md
│  ├── deploy.md
│  ├── maintenance-checklist.md
│  ├── monitoring.md
│  ├── reports.md
│  └── tasks-workflow.md
├── examples
│  ├── 'Financial Report by Pesarifu for John Mwangi.pdf'
│  └── mpesa.pdf
├── services
│  └── app.service
├── src
│  ├── pesarifu
│  │  ├── api
│  │  │  ├── __init__.py
│  │  │  └── app.py
│  │  ├── config
│  │  │  ├── celery.py
│  │  │  ├── config.py
│  │  │  └── settings.toml
│  │  ├── db                                # data model
│  │  │  ├── load.py
│  │  │  ├── models.py
│  │  │  ├── seed.py
│  │  │  └── util.py
│  │  ├── etl
│  │  │  ├── safaricom
│  │  │  │  ├── __init__.py
│  │  │  │  ├── details_grammar.ebnf
│  │  │  │  ├── extract.py
│  │  │  │  ├── load.py
│  │  │  │  ├── tasks.py
│  │  │  │  └── transform.py
│  │  │  ├── stanchart
│  │  │  └── __init__.py
│  │  ├── templates
│  │  │  ├── base.html
│  │  │  ├── email-report.html.jinja
│  │  │  ├── error.html
│  │  │  ├── index.html
│  │  │  ├── privacy-policy.html
│  │  │  └── success.html
│  │  └── util
│  │     ├── export.py                      # functions for exporting transactions to various formats
│  │     ├── helpers.py
│  │     ├── notify.py
│  │     └── tasks.py
│  ├── reports                              # Evidence Report Generation
│  │  ├── components
│  │  │  ├── Logo.svelte
│  │  │  ├── MyHeader.svelte
│  │  │  └── pesarifu-logo.svg
│  │  ├── pages
│  │  │  ├── +layout.svelte
│  │  │  ├── [user_uuid].md
│  │  │  └── users.md
│  │  ├── partials
│  │  │  ├── account-comparison.md
│  │  │  └── period-comparison.md
│  │  ├── sources
│  │  │  └── pesarifu
│  │  │     ├── accounts.sql
│  │  │     ├── connection.yaml
│  │  │     └── transactions.sql
│  │  ├── evidence.plugins.yaml
│  │  ├── package-lock.json
│  │  ├── package.json
│  │  └── README.md
│  └── website                              # Landing Page
├── static
│  └── src
│     └── input.css
├── tests
│  ├── __init__.py
│  └── test_details_parser.py
├── alembic.ini
├── Caddyfile                               # reverse proxy configuration for web server
├── justfile                                # project related tasks
├── package-lock.json
├── package.json
├── pyproject.toml
├── README.md
└── tailwind.config.js
```
