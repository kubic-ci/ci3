"""
kubic-ci command line interface called `kubic`.

See:
    setup.py
"""
from .version import __version__


BOX = u'\u2B1C'
PROMPT = u'{box}: kubic-ci {version}'.format(box=BOX, version=__version__)


def main():
    """Entry point for the CLI."""
    # Print prompt at the start, always.
    print(PROMPT)
