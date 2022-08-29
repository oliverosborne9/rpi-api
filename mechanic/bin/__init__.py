import click


@click.command()
def cli():
    """
    Command line interface to start Flask server
    to handle weighing and dispensing tasks.
    """
    from mechanic.api.launch import start_app

    start_app()
