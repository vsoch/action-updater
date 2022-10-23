#!/usr/bin/env python

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import argparse
import os
import sys

import action_updater
from action_updater.logger import setup_logger


def get_parser():
    parser = argparse.ArgumentParser(
        description="Actions Updater",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Global Variables
    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--quiet",
        dest="quiet",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="show software version.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--settings-file",
        dest="settings_file",
        help="custom path to settings file.",
    )

    # On the fly updates to config params
    parser.add_argument(
        "-c",
        dest="config_params",
        help=""""customize a config value on the fly to ADD/SET/REMOVE for a command
action-updater -c set:key:value <command> <args>
action-updater -c add:listkey:value <command> <args>
action-updater -c rm:listkey:value""",
        action="append",
    )

    subparsers = parser.add_subparsers(
        help="actions",
        title="actions",
        description="actions",
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", description="show software version")
    subparsers.add_parser("list-updaters", description="list updaters available")

    # Detect changes for a directory or file of interest
    detect = subparsers.add_parser(
        "detect",
        description="detect action updates before applying them.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    update = subparsers.add_parser(
        "update",
        description="detect and apply updates.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    for command in detect, update:
        command.add_argument(
            "paths",
            help="path to run detect over (e.g., yaml file or GitHub actions folder)",
            action="append",
        )
        command.add_argument(
            "-u",
            "--updater",
            dest="updaters",
            help="update using one or more specific updaters",
            action="append",
        )
        command.add_argument(
            "--updaters",
            dest="updater_list",
            help="provide a comma separated value list of updater (e.g., version,setoutput)",
        )
        command.add_argument(
            "--no-details",
            dest="no_details",
            help="do not show details for file changes",
            default=False,
            action="store_true",
        )

    config = subparsers.add_parser(
        "config",
        description="update configuration settings. Use set or get to see or set information.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    config.add_argument(
        "--central",
        dest="central",
        help="make edits to the central config file.",
        default=False,
        action="store_true",
    )

    config.add_argument(
        "params",
        nargs="*",
        help="""Set or get a config value, edit the config, add or remove a list variable, or create a user-specific config.
action-updater config set key value
action-updater config set key:subkey value
action-updater config get key
action-updater edit
action-updater config inituser
action-updater config add registry /tmp/registry
action-updater config remove registry /tmp/registry""",
        type=str,
    )

    return parser


def run_action_updater():

    parser = get_parser()

    def help(return_code=0):
        """print help, including the software version and active client
        and exit with return code.
        """

        version = action_updater.__version__

        print("\nSingularity Registry (HPC) Client v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    if args.debug is True:
        os.environ["MESSAGELEVEL"] = "DEBUG"

    # Show the version and exit
    if args.command == "version" or args.version:
        print(action_updater.__version__)
        sys.exit(0)

    setup_logger(
        quiet=args.quiet,
        debug=args.debug,
    )

    # retrieve subparser (with help) from parser
    helper = None
    subparsers_actions = [
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    ]
    for subparsers_action in subparsers_actions:
        for choice, subparser in subparsers_action.choices.items():
            if choice == args.command:
                helper = subparser
                break

    if args.command == "detect":
        from .detect import main
    elif args.command == "config":
        from .config import main
    elif args.command == "update":
        from .update import main
    elif args.command == "list-updaters":
        from .listing import list_updaters as main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, parser=parser, extra=extra, subparser=helper)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    run_action_updater()
