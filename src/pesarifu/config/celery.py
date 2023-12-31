from celery import Celery
from dotenv import dotenv_values

config = dotenv_values()
broker = config["CELERY_BROKER_URL"]
backend = config["CELERY_RESULTS_BACKEND"]

app = Celery(
    "pesarifu_tasks",
    broker=broker,
    backend=backend,
    include=["pesarifu.etl.safaricom.tasks"],
)
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
