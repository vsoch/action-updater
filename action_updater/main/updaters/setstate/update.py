__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.main.updater import UpdaterBase
from action_updater.main.updaters.setoutput.update import update_lines


class SetstateUpdater(UpdaterBase):

    name = "set-state"
    description = "update deprecated set-state commands"

    def detect(self, action):
        """
        Detect changes in an action, old set-state.
        """
        # Set the count to 0
        self.count = 0
        updated = False

        # No point if we don't have jobs!
        if not action.jobs:
            return

        # For each job, look for steps->updater versions
        for _, job in action.jobs.items():
            for step in job.get("steps", []):

                # We are primarily interested in uses
                if "run" not in step:
                    continue

                # Update step run lines
                updated_lines = update_lines(step["run"], "set-state", "$GITHUB_STATE")
                updated = updated or (updated_lines != step["run"])
                step["run"] = updated_lines

        return updated
