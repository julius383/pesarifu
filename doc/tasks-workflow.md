# Tasks Workflow

The back-end makes use of [celery][1] for task execution. Celery serves the
dual purpose of:

- offloading work from the main thread
- providing an easy way to scale the application without needing to run
  multiple instances in the early-mid stages

Each separate provider needs to define tasks relevant to it and have an entry
point for processing each source type supported. See
`src/pesarifu/etl/safaricom/tasks.py` and `src/pesarifu/etl/safaricom/__init__.py` relative to the project root.

Use [flower][2] for monitoring tasks in celery



[1]: https://docs.celeryq.dev/en/stable/getting-started/introduction.html
[2]: https://flower.readthedocs.io/en/latest/
