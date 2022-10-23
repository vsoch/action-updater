__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


import string

import pipelib.pipeline as pipeline
import pipelib.steps as step


def sort_tags(tags):
    """
    Sort a list of string tags, return sorted (first latest) with original version
    """
    # all letters excluded except for v
    letters = "(%s)" % "|".join([x for x in string.ascii_letters if x not in ["v", "V"]])

    # A pipeline to process docker tags
    steps = (
        # No letters except for "v"
        ~step.filters.HasPatterns(filters=[letters]),
        # Scrub commits from version string
        step.filters.CleanCommit(),
        # Parse versions, return sorted ascending, and taking version major.minor.patch into account
        step.container.ContainerTagSort(),
    )
    p = pipeline.Pipeline(steps)
    return p.run(list(tags), unwrap=False)


def sort_major(tags):
    """
    Allow major tags like v3
    """
    # A pipeline to process docker tags
    steps = step.release.MajorTagSort()
    p = pipeline.Pipeline(steps)
    return p.run(list(tags), unwrap=False)
