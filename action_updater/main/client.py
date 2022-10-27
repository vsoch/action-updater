__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import os

from rich.console import Console

import action_updater.utils as utils

from .action import GitHubAction
from .settings import Settings
from .updater import UpdaterFinder


class ActionUpdater:
    """
    Create a GitHub updater
    """

    def __init__(self, quiet=False, token=None, settings_file=None, **kwargs):
        self.token = token
        self._updaters = {}
        self.quiet = quiet
        self.c = Console()

        # If using for a GitHub action, a global flag that indicates changes
        self.has_changes = False

        # If we don't have default settings, load
        if not hasattr(self, "settings"):
            self.settings = Settings(settings_file)

    @property
    def updaters(self):
        """
        Get a list of updaters available
        """
        if not self._updaters:

            # All updaters can be provided with the GitHub token
            self.finder = UpdaterFinder()
            self._updaters = {}
            for name, updaterClass in self.finder.items():

                # Instantiate an updater for the path, provide settings
                self._updaters[name] = updaterClass(token=self.token, settings=self.settings)

        return self._updaters

    def iter_paths(self, paths):
        """
        Helper function to flexibly handle parsing paths.
        """
        # Ensure we start from a list
        if not isinstance(paths, list):
            paths = [paths]

        final = set()

        # Run each updater on each path
        for path in paths:

            if os.path.exists(path) and os.path.isfile(path):
                final.add(path)
                continue
            for filename in utils.recursive_find(path, "[.](yaml|yml)"):
                final.add(filename)
        return list(final)

    def detect(self, paths, details=True, updaters=None):
        """
        Look for changes in files according to updaters
        """
        actions = {}

        for path in self.iter_paths(paths):

            # Load into GitHub action
            action = GitHubAction(path)

            self.c.print(f"⭐️ [yellow]{path}[/yellow]")

            # Todo convert this into an iter function (shared between detect and update)
            for _, updater in self.updaters.items():

                # Skip updaters per request of the user
                if updaters and updater.slug not in updaters:
                    continue

                # The count reflects the last run
                if updater.detect(action):
                    self.c.print(f"[red]✖️ {updater.title} Updater: {updater.count} updates[/red]")
                    self.has_changes = True
                else:
                    self.c.print(f"[green]✔ {updater.title}: No updates[/green]")

            # If we want to show details:
            if details:
                action.diff(self.settings.code_theme or "vim")
            actions[path] = action
        return actions

    def update(self, paths, details=True, updaters=None):
        """
        Update files.
        """
        actions = self.detect(paths, details=details, updaters=updaters)
        for path, action in actions.items():
            if action.has_changes:
                self.c.print(f"[purple]❇ Writing updated {path}[/purple]")
                action.write(path, line_length=self.settings.line_length)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[action-updater]"
