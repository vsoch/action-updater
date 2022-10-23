__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"

from action_updater.main.github import sort_major, sort_tags
from action_updater.main.updater import UpdaterBase

schema = {
    "type": "object",
    "properties": {
        # Allow these orgs to use major version strings
        "major_orgs": {"type": "array", "items": {"type": "string"}}
    },
    "additionalProperties": False,
}


def update_comment(comment_list, comment):
    """
    Update an old comment to a new one
    """
    updated = False
    items = []
    for item in comment_list:
        if item and hasattr(item, "value") and not updated:
            item.value = f"# {comment}\n"
            updated = True
        items.append(item)
    return items


class VersionUpdater(UpdaterBase):

    name = "version"
    description = "update action versions"
    schema = schema
    cache = {"tags": {}}

    def detect(self, action):
        """
        Detect changes (to be later saved)
        """
        # Set the count to 0
        self.count = 0

        # No point if we don't have jobs!
        if not action.jobs:
            return

        # We will use major versions for these orgs (trusted)
        trusted_orgs = self.settings.get("major_orgs")

        # For each job, look for steps->updater versions
        for job_name, job in action.jobs.items():
            for step in job.get("steps", []):

                # We are primarily interested in uses
                if "uses" not in step:
                    continue

                repo = step["uses"]

                # If we have a local action, nothing to update
                if repo.startswith("./"):
                    continue

                # Get the current tag or version (we will want to maintain this convention)
                # Create a lookup based on the ref
                repo, tag = repo.split("@")
                org, _ = repo.split("/", 1)

                # Retrieve all tags for the repository, a lookup by tag name
                tags = self.cache["tags"].get(repo) or self.get_tags_lookup(repo)

                updated = None
                if trusted_orgs and org in trusted_orgs:
                    updated = self.get_major_tag(tags)

                if not updated:
                    updated = self.get_tagged_commit(tags)

                if not updated:
                    continue
                updated = f"{repo}@{updated}"

                if updated != step["uses"]:
                    # If we added a new comment, update the old one
                    if "#" in updated and "uses" in step.ca.items:
                        updated, comment = updated.split("#", 1)
                        step.ca.items["uses"] = update_comment(step.ca.items["uses"], comment)
                    step["uses"] = updated.strip()
                    self.count += 1
        return True

    def get_major_tag(self, tags):
        """
        Given a list of repository tags, get the most up-todate!
        """
        # If we have a major org, we trust it and want the major version tag
        tags_list = list(tags)
        tags_list = [x for x in tags_list if "." not in x]

        # Cut out early if we don't have major-only tags
        if not tags_list:
            return []

        # Get ordered major tags
        ordered = sort_major(tags_list)

        # If we don't have ordered, we could use branches, but skip for now
        if not ordered:
            return []

        tag = ordered[0]._original

        # Use latest release verbatim
        return tag

    def get_tagged_commit(self, tags):
        """
        Given a list of repository tags, get the most up-todate!
        """
        # Get ordered major tags
        ordered = sort_tags(list(tags))

        # If we don't have ordered, we could use branches, but skip for now
        if not ordered:
            return []

        tag = ordered[0]._original
        meta = tags[tag]
        commit = meta["object"]["sha"]
        return f"{commit} # {tag}"
