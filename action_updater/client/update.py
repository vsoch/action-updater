__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.main import get_client


def main(args, parser, extra, subparser):
    cli = get_client(quiet=args.quiet)
    cli.update(paths=args.paths, details=not args.no_details, updaters=args.updaters)
