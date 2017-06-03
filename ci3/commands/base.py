import argparse


class CliCommand(object):
    """Base class for cli commands."""

    def add_arguments(self, subparser):
        """(Optional) add cli arguments to the subparser."""

    def run(self, args):
        """Do actual work when running the command."""
        raise NotImplementedError()


class CommandLineInterface(object):
    """CLI abstraction."""

    def __init__(self, parser):
        """Initialize CLI class."""
        self.parser = parser
        self.subparsers = self.parser.add_subparsers()

    def add_command(self, name, cls):
        """Add command to handle subparsed results of the cli."""
        # Instantiate passed command class. It will get the parsed arguments
        # passed in case the command is invoked from the cli.
        command = cls()
        subparser = self.subparsers.add_parser(name)
        command.add_arguments(subparser)
        subparser.set_defaults(func=command.run)

    def run(self):
        """Run respective command to handle parsed arguments."""
        args = self.parser.parse_args()
        args.func(args)
