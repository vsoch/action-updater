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
        if not action.steps:
            return False

        # We will use major versions for these orgs (trusted)
        trusted_orgs = self.settings.get("major_orgs")

        # For each job, look for steps->updater versions
        for step in action.steps:

            # We are primarily interested in uses
            if "uses" not in step:
                continue

            repo = step["uses"]

            # If we have a local action, nothing to update
            if repo.startswith("./"):
                continue

            # Get the current tag or version (we will want to maintain this convention)
            # Create a lookup based on the ref
            repo, _ = repo.split("@")
            org, _ = repo.split("/", 1)

            # Retrieve all tags for the repository, a lookup by tag name
            tags = self.cache["tags"].get(repo) or self.get_tags_lookup(repo)

            updated = None
            if trusted_orgs and org in trusted_orgs:
                updated = self.get_major_tag(tags)

            if not updated:
                updated = self.get_tagged_commit(tags)

            # Save repo tags in cache
            self.cache["tags"][repo] = tags

            # If we don't have tags by this point, no go - we cannot parse
            if not updated:
                continue
            updated = f"{repo}@{updated}"
            previous = step["uses"]

            # If we added a new comment, update the old one
            if "#" in updated:
                updated, comment = updated.split("#", 1)
                comment = comment.strip()
                step["uses"] = updated.strip()

                # TODO some check to preserve other previous comments?
                step.ca.items["uses"] = [None, None, None, None]

                # Add the end of line comment (third position in list)
                step.yaml_add_eol_comment(f"# {comment}\n", "uses", column=0)

            # Always do the update (regardless of comment!)
            step["uses"] = updated.strip()

            # Do we have a change?
            if step["uses"] != previous:
                self.count += 1

        return self.count != 0

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

        # First pass - no ordered tags, try to do the same for the major versions
        if not ordered:
            ordered = sort_major(tags)

        # If we don't have ordered, we could use branches, but skip for now
        if not ordered:
            return []

        tag = ordered[0]._original
        meta = tags[tag]
        commit = meta["object"]["sha"]
        return f"{commit} # {tag}"
