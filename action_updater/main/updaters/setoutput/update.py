__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

import re

from action_updater.main.updater import UpdaterBase


def update_lines(lines, key="set-output", envar="$GITHUB_OUTPUT"):
    """
    Helper function to replace generic "set-X" variable with pipe to envar.
    """
    lines = lines.splitlines(keepends=True)

    updated = []

    for line in lines:
        if key not in line:
            updated.append(line)
            continue

        # Convert:
        # echo "::set-output name={name}}::${raw_data[4]}"
        # echo "name=value" >> $GITHUB_OUTPUT
        match = re.search("%s(\s)+name=(?P<name>.+)::(?P<value>.+)" % key, line)  # noqa
        if not match:
            updated.append(line)
            continue

        match = match.groupdict()
        value = match["value"].strip('"').strip("'")
        line = 'echo "%s=%s" >> %s' % (match["name"], value, envar)
        updated.append(line)

    return "".join(updated)


class SetoutputUpdater(UpdaterBase):

    name = "set-output"
    description = "update deprecated set-output commands"

    def detect(self, action):
        """
        Detect changes in an action, old set-output.
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

                # Update step run lines (returns parsed again together)
                updated_lines = update_lines(step["run"])
                updated = updated or (updated_lines != step["run"])
                step["run"] = updated_lines

        return updated
