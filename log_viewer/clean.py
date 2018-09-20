

import click
from flask import current_app, g
from flask.cli import with_appcontext

from . import log_viewer


@click.command('clean')
@with_appcontext
def clean_command():
    """Clear the directory structure."""
    run_dir = current_app.config[ 'BASE_DIR' ] 
    lv = log_viewer.LogViewer( run_dir )
    lv.clean()

    click.echo('Cleaned up directories.')


def init_app(app):
    app.cli.add_command( clean_command )
