from celery import Celery

from pesarifu.config.config import settings

broker = settings["CELERY_BROKER_URL"]
backend = settings["CELERY_RESULTS_BACKEND"]

app = Celery(
    "pesarifu_tasks",
    broker=broker,
    backend=backend,
    include=["pesarifu.etl.safaricom", "pesarifu.util.tasks"],
)
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
