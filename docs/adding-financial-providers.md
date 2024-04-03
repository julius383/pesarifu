# How to add new financial providers

- Open sample statement in `PDFBox` using the command:

```sh
pdfbox PDFDebugger examples/mpesa_statement_export.pdf
```

- Figure out extraction strategy for account info if contained using
  `pdftotext` and `sed`
- Figure out the x values and column names for the columns in the table
- Decide whether there are any columns with entries spread across multiple
  rows
- create in `src/pesarifu/etl/[provider-name]/extract.py` the functions
  `get_transactions_from_pdf` and `get_metadata_from_pdf`. See
  `src/pesarifu/etl/safaricom/extract.py` for example
- in `src/pesarifu/etl/[provider-name]/extract.py` also create:
    - `transform.py` for cleaning and processing extracted transactions
    - `tasks.py` celery tasks for the provider
    - `load.py` for adding transaction to database
    - `__init__.py` exporting `go(pdf_path, metadata)` that runs the celery
      tasks for handling transactions for this provider.
