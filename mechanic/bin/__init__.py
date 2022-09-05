import click
from mechanic.api.launch import setup_app, start_app


@click.command()
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    default="config.json",
    show_default=True,
    help="Path to JSON config file.",
)
def cli(config):
    """
    Command line interface to start Flask server
    to handle weighing and dispensing tasks.
    """

    app = setup_app(config_path=config)
    start_app(app)
