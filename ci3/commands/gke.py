"""Google Container Engine (GKE) cli command."""
from sh import ErrorReturnCode, gcloud
from .base import CliCommand


class GkeCommand(CliCommand):
    """Interface Google Container Engine (GKE) to create k8s clusters."""

    def add_arguments(self, subparser):
        """
        Add cli arguments to the subparser.

        Note if you need only first level argument, then don't implement it.
        """

    def run(self, args):
        """Execute command."""
        try:
            res = gcloud('container')
        except ErrorReturnCode as error:
            print(error)
