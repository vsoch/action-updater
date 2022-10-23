__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


def parse_updaters(args):
    """
    Parse a unique set of updaters from --update and --updaters
    """
    updaters = args.updaters or []
    if args.updater_list:
        updaters += [x.strip() for x in args.updater_list.split(",") if x.strip()]
    return list(set(updaters))
