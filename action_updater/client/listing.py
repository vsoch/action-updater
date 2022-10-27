__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.logger import Table
from action_updater.main import get_client


def list_updaters(args, parser, extra, subparser):
    cli = get_client(quiet=args.quiet)

    # Update config settings on the fly
    cli.settings.update_params(args.config_params)

    items = [
        {"title": x.title, "identifier": name, "description": x.description}
        for name, x in cli.updaters.items()
    ]
    table = Table(items)
    table.show()
