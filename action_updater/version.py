__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.0.16"
AUTHOR = "Vanessa Sochat"
EMAIL = "vsoch@users.noreply.github.com"
NAME = "action-updater"
PACKAGE_URL = "https://github.com/vsoch/action-updater"
KEYWORDS = "github, actions, updater"
DESCRIPTION = "Update deprecated command, versions, and other for GitHub actions"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("pipelib", {"min_version": None}),
    ("jsonschema", {"min_version": None}),
    # Required to maintain comments in files
    ("ruamel.yaml", {"min_version": None}),
    ("rich", {"min_version": None}),
    ("pyyaml", {"min_version": None}),
    ("requests", {"min_version": None}),
    # seems to be an issue for older python
    ("packaging", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

################################################################################
# Submodule Requirements (versions that include database)

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
