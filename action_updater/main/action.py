__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


import copy
import difflib

from rich.console import Console
from rich.markdown import Markdown

import action_updater.utils as utils


class GitHubAction:
    """
    Parse a GitHub action into it's sections.

    We always present the changes (copy of original) and then can
    easily compare the two. The overall structure should not change.
    """

    def __init__(self, filename):
        self.cfg = utils.read_yaml(filename)
        self.changes = copy.deepcopy(self.cfg)

    @property
    def jobs(self):
        return self.changes.get("jobs")

    @property
    def runs(self):
        return self.changes.get("runs")

    @property
    def steps(self):
        if self.jobs:
            for _, job in self.jobs.items():
                for step in job.get("steps", []):
                    yield step

        elif self.runs:
            for step in self.runs.get("steps", []):
                yield step

    def write(self, path, line_length=None):
        """
        Save the action to file.
        """
        utils.write_yaml(self.changes, path, line_length)

    @property
    def has_changes(self):
        """
        Determine if before != after (the action has changed)
        """
        return self.render_before() != self.render_after()

    def render_after(self):
        """
        Render the action post-detect (with changes).
        """
        return utils.get_yaml_string(self.changes).splitlines(keepends=True)

    def render_before(self):
        """
        Render the action pre-detect (without changes).
        """
        return utils.get_yaml_string(self.cfg).splitlines(keepends=True)

    def diff(self, code_theme="vim"):
        """
        Show diff between original (cfg) and changed!
        """
        before = self.render_before()
        after = self.render_after()

        if before == after:
            print()
            return

        diff = "".join(
            list(
                difflib.unified_diff(
                    before,
                    after,
                    "original",
                    "updated",
                )
            )
        )

        c = Console()
        md = Markdown(f"""\n```diff\n{diff}\n```\n""", code_theme=code_theme)
        c.print(md)
