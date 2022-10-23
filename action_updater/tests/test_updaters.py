#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import string

import pytest

from action_updater.main.action import GitHubAction
from action_updater.tests.helpers import get_updaters, here, init_client


@pytest.mark.parametrize("updater_name", get_updaters())
def test_updaters(tmp_path, updater_name):
    """
    Test each updater.
    """
    client = init_client(str(tmp_path))
    updater = client.updaters[updater_name]

    # The updater must have a description and title
    assert updater.description
    assert updater.title

    # The name must be all lowercase, no special characters except for -
    letters = string.ascii_letters + "-"
    for letter in updater.name:
        assert letter in letters

    # A test (before and after) must be defined for each
    before_file = os.path.join(here, "data", f"{updater.name}-before.yaml")
    after_file = os.path.join(here, "data", f"{updater.name}-after.yaml")
    for filename in before_file, after_file:
        assert os.path.exists(filename)

    # Count is 0 before run, and we find changes
    assert updater.count == 0

    # Read into GitHub action
    action = GitHubAction(before_file)

    # Run the whole thing with detect (to print to console)
    result = client.detect(before_file, updaters=[updater.slug])
    result[before_file].render_after() == action.render_after()

    result = updater.detect(action)
    assert result is True
    assert action.has_changes

    # Count is 0 before run, and we find changes
    assert updater.count != 0

    # Now for the after file (shouldn't change until GitHub updates versions, slowly)
    action = GitHubAction(after_file)
    result = updater.detect(action)
    assert result is False
