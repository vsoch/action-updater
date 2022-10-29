__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.main.updater import UpdaterBase
from action_updater.main.updaters.setoutput.update import update_lines


class SavestateUpdater(UpdaterBase):

    name = "save-state"
    description = "update deprecated save-state commands"

    def detect(self, action):
        """
        Detect changes in an action, old set-state.
        """
        # Set the count to 0
        self.count = 0

        # No point if we don't have jobs!
        if not action.steps:
            return False

        # For each job, look for steps->updater versions
        for step in action.steps:

            # We are primarily interested in uses
            if "run" not in step:
                continue

            # Update step run lines
            updated_lines = update_lines(step["run"], "save-state", "$GITHUB_STATE")

            # Keep track of change counts
            if updated_lines != step["run"]:
                self.count += 1

            step["run"] = updated_lines

        return self.count != 0
