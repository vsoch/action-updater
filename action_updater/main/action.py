__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


import action_updater.utils as utils
import difflib
from rich.markdown import Markdown
from rich.console import Console
import copy


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

    def write(self, path):
        """
        Save the action to file.
        """
        utils.write_yaml(self.changes, path)

    def has_changes(self):
        """
        Determine if before != after (the action has changed)
        """
        before = utils.get_yaml_string(self.cfg).splitlines(keepends=True)
        after = utils.get_yaml_string(self.changes).splitlines(keepends=True)
        return before != after

    def diff(self):
        """
        Show diff between original (cfg) and changed!
        """
        before = utils.get_yaml_string(self.cfg).splitlines(keepends=True)
        after = utils.get_yaml_string(self.changes).splitlines(keepends=True)

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
        md = Markdown(f"""\n```diff\n{diff}\n```\n""", code_theme="vim")
        c.print(md)
