__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.logger import logger
from action_updater.main import get_client

from .helpers import parse_updaters


def main(args, parser, extra, subparser):
    cli = get_client(quiet=args.quiet)
    cli.detect(paths=args.paths, details=not args.no_details, updaters=parse_updaters(args))
    if cli.has_changes:
        logger.exit("Found changes, exiting with non-zero code.")
