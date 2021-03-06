#! /usr/bin/env python3
import sys

import appdirs
import click
import click_repl

from .android import android
from .config import config_command
from .dev import dev
from .images import images_command
from .k8s import k8s
from .local import local
from .plugins import plugins_command, add_plugin_commands
from .ui import ui
from .webui import webui
from ..__about__ import __version__
from .. import exceptions
from .. import fmt


# pylint: disable=too-few-public-methods
class Context:
    def __init__(self, root):
        self.root = root


def main():
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except exceptions.TutorError as e:
        fmt.echo_error("Error: {}".format(e.args[0]))
        sys.exit(1)


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
@click.version_option(version=__version__)
@click.option(
    "-r",
    "--root",
    envvar="TUTOR_ROOT",
    default=appdirs.user_data_dir(appname="tutor"),
    show_default=True,
    type=click.Path(resolve_path=True),
    help="Root project directory (environment variable: TUTOR_ROOT)",
)
@click.pass_context
def cli(context, root):
    context.obj = Context(root)


@click.command(help="Print this help", name="help")
def print_help():
    with click.Context(cli) as context:
        click.echo(cli.get_help(context))


click_repl.register_repl(cli, name="ui")
cli.add_command(images_command)
cli.add_command(config_command)
cli.add_command(local)
cli.add_command(dev)
cli.add_command(android)
cli.add_command(k8s)
cli.add_command(ui)
cli.add_command(webui)
cli.add_command(print_help)
cli.add_command(plugins_command)
add_plugin_commands(cli)

if __name__ == "__main__":
    main()
