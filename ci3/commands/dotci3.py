"""Status cli command."""
import os
from ci3.error import Ci3Error
from .base import CliCommand


class MissingDotCi3Folder(Ci3Error):
    """"Raised if project not initialized and `.ci3` is missing."""


class DotCi3Mixin(object):
    """Help with `.ci3` folder project configuration."""

    @property
    def dotci3_path(self):
        """Return fullpath string to `.ci3` folder."""
        return os.path.join(os.getcwd(), '.ci3')

    def get_dotci3_path(self):
        """Return fullpath to `.ci3` if exists or raise error."""
        path = os.path.join(os.getcwd(), '.ci3')
        if not os.path.exists(path):
            raise MissingDotCi3Folder("Missing `.ci3` folder. Have you tried "
                                      "`kubic init` ?")
        return path

    @property
    def secrets_path(self):
        """Return fullpath string to `.ci3/secrets` folder."""
        return os.path.join(self.dotci3_path, 'secrets')


class StatusCommand(CliCommand, DotCi3Mixin):
    """Report status of ci3 project."""

    def run(self, args):
        """
        Report status of the project based on the content of `.ci3` folder.

        If not folder is found advice to call `init` command.
        """
        print('kubic-ci project ({})'.format(self.get_dotci3_path()))


class InitCommand(CliCommand, DotCi3Mixin):
    """Report status of ci3 project."""

    def run(self, args):
        """
        Report status of the project based on the content of `.ci3` folder.

        If not folder is found advice to call `init` command.
        """
        if os.path.exists(self.dotci3_path):
            print('kubic-ci project has been already initialized..Skipping')
            return
        print('Initializing kubic-ci project configuration: {}'
              .format(self.dotci3_path))

        # Init secrets folder
        os.makedirs(self.secrets_path)
        with open(os.path.join(self.secrets_path, '.gitignore'), 'w+') as gi:
            gi.write('# Place your keys and secrets here, but never commit')
