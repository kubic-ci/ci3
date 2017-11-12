"""Docker commands."""
import sys
import logging
from sh import docker, ErrorReturnCode

from .base import CliCommand
from .dotci3 import DotCi3Mixin
from ci3.error import Ci3Error


logger = logging.getLogger(__name__)


class BuildCommand(CliCommand, DotCi3Mixin):
    """Build container images with docker."""

    def run(self, args):
        """Call docker to build image."""
        self.load_vars()
        for name in self.config_vars['containers']:
            values = self.config_vars['containers'][name]
            image_registry_url = self.config_vars['cluster']['image_registry_url']
            tag = "{}/{}:{}".format(
                image_registry_url,
                values['image']['name'],
                values['image']['tag'])
            try:
                logger.info('Building %s..' % name)
                docker.build('-t', tag, '.', _out=sys.stdout, _err=sys.stderr)
                logger.info('Done')
            except ErrorReturnCode as error:
                raise Ci3Error("Failed to build docker image `{}`: {}"
                               .format(name, error))


class PushCommand(CliCommand, DotCi3Mixin):
    """Push container images to docker registry."""

    def run(self, args):
        """Call docker to push image."""
        self.load_vars()
        for name in self.config_vars['containers']:
            values = self.config_vars['containers'][name]
            image_registry_url = self.config_vars['cluster']['image_registry_url']
            tag = "{}/{}:{}".format(
                image_registry_url,
                values['image']['name'],
                values['image']['tag'])
            try:
                logger.info('Pushing %s..' % tag)
                docker.push(tag, _out=sys.stdout, _err=sys.stderr)
                logger.info('Done')
            except ErrorReturnCode as error:
                raise Ci3Error("Failed to push docker image `{}`: {}"
                               .format(tag, error))
