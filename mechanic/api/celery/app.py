from threading import Thread

from celery import Celery

REDIS_CONNECTION_STRING = "redis://redis:6379/0"


def make_celery() -> Celery:
    """
    Initialise a Celery app object, using a Redis database as backend and broker.
    Depends on a running Redis database, working with defaults from official Redis Docker image.
    """
    # Container name and therefore host redis, exposed port for db 6379, hence redis:6379
    celery_app = Celery(backend=REDIS_CONNECTION_STRING, broker=REDIS_CONNECTION_STRING)
    celery_app.conf.update(
        {
            "imports": ("mechanic.api.celery.tasks"),
            "task_serializer": "json",
            "result_serializer": "json",
            "accept_content": ["json"],
            "worker_concurrency": 1,
            "result_backend": REDIS_CONNECTION_STRING,
        },
    )
    return celery_app


# This constant is used to decorate Celery tasks and to start the worker
CELERY_APP = make_celery()


def start_bg_celery_worker():
    """
    Start a Celery worker to serve the tasks,
    using threading to not block the main process
    (launching the Flask server).
    """

    thread = Thread(target=lambda: CELERY_APP.Worker().start(), daemon=True)
    # Daemon, so if the main process fails, the Python program exits
    # (and is not left hanging by running Celery worker thread)
    thread.start()
