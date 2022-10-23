__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


import abc
import importlib
import inspect
import os
import re
from collections.abc import Mapping

import jsonschema
import requests

from action_updater.logger import logger

here = os.path.abspath(os.path.dirname(__file__))


class UpdaterFinder(Mapping):
    """
    Create a cache of available updaters.
    """

    _updaters = {}

    def __init__(self):
        """
        Instantiate an updater
        """
        self.collection_path = os.path.join(here, "updaters")
        self.load()

    def __getitem__(self, name):
        return self._updaters.get(name)

    def __iter__(self):
        return iter(self._updaters)

    def __len__(self):
        return len(self._updaters)

    def load(self):
        """
        Load new updaters
        """
        self._updaters = self._load_updaters()

    def _load_updaters(self):
        """
        Load updaters based on listing folders in the collection.
        """
        lookup = {}
        for name in os.listdir(self.collection_path):
            updater_dir = os.path.join(self.collection_path, name)
            updater_file = os.path.join(updater_dir, "update.py")

            # Skip files in collection folder
            if os.path.isfile(updater_dir):
                continue

            # Continue if the file doesn't exist
            if not os.path.exists(updater_file):
                logger.debug("%s does not appear to have an update.py, skipping." % updater_dir)
                continue

            # The class name means we split by underscore, capitalize, and join
            class_name = "".join([x.capitalize() for x in name.split("_")]) + "Updater"
            module = "action_updater.main.updaters.%s.update" % name

            # Not instantiated - will be instantiated for a specific action
            lookup[name] = getattr(importlib.import_module(module), class_name)
        return lookup


class UpdaterBase:

    name = "updater"
    description = "An abstract base updater."
    date_time_format = "%Y-%m-%dT%H:%M:%S%z"

    # The default updater is not intended for static files
    static_files = False

    def __init__(self, token, settings=None):
        self._data = {}
        self.headers = {}
        self.update_token(token)
        self.count = 0

        # Each updater can ship its own settings schema
        if not hasattr(self, "schema"):
            self.schema = {}

        self.validate_settings(settings)

    @abc.abstractmethod
    def detect(self, *args, **kwargs):
        pass

    @property
    def slug(self):
        return re.sub("(-|_)", "", self.name)

    @property
    def title(self):
        return self.name.capitalize()

    def validate_settings(self, settings):
        """
        If settings are provided (and the updater has a schema) ensure we validate.
        """
        self.global_settings = settings or {}
        if self.global_settings and self.schema:
            jsonschema.validate(self.settings, schema=self.schema)

    @property
    def settings(self):
        """
        Get settings specific to updater
        """
        return self.global_settings.updaters.get(self.name, {})

    def update_token(self, token=None):
        """
        Set token and headers, if found
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if self.token:
            self.headers["Authorization"] = "token %s" % self.token

    @property
    def classpath(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def get_releases(self, repo):
        """
        Get the lateset release of an action (under flux-framework)
        """
        return self.get_request(f"{self.global_settings.github_api}/repos/{repo}/releases")

    def get_tags(self, repo):
        """
        Get the lateset tags for a repository
        """
        return self.get_request(f"{self.global_settings.github_api}/repos/{repo}/git/refs/tags")

    def get_tags_lookup(self, repo):
        """
        This isn't required to be sploot out, but it's easier to debug / read if necessary
        """
        tags = {}
        for t in self.get_tags(repo):
            if "ref" not in t or "refs/tags" not in t["ref"]:
                continue
            tags[re.sub("refs/tags/", "", t["ref"])] = t
        return tags

    def get_request(self, url):
        """
        Perform a GitHub get request (assume pagination)
        """
        response = requests.get(url, headers=self.headers, params={"per_page": 100})

        try:
            response.raise_for_status()
        except Exception:
            # Set a warning about limtis without tokens!
            if not self.token:
                logger.exit("export GITHUB_TOKEN to increase API limits.")

        # latest release should be first in this set
        return response.json()
