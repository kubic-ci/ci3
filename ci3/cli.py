"""
kubic-ci command line interface called `kubic`.

See:
    setup.py
"""
import argparse

from ci3.commands.base import CommandLineInterface
from ci3.commands.gke import GkeCommand
from ci3.version import __version__


BOX = u'\u2B1C'
PROMPT = u'{box}: kubic-ci {version}'.format(box=BOX, version=__version__)


def main():
    """Entry point for the CLI."""
    # Print prompt at the start, always.
    parser = argparse.ArgumentParser(description=PROMPT)
    cli = CommandLineInterface(parser)

    # Add arguments shared between commands.
    cli.parser.add_argument('-v', '--verbose', dest='verbose',
                            action='count', default=1)

    # Add commands with respective subcommands. See run method of each class.
    cli.add_command('gke', GkeCommand)

    # Parse cli arguments and execute respective command to handle them.
    cli.run()
