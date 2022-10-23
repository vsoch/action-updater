#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil

from action_updater.main import get_client

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def init_client(tmpdir):
    """
    Get a common client for some container technology and module system
    """
    settings_file = os.path.join(root, "settings.yml")
    new_settings = os.path.join(tmpdir, "settings.yml")
    shutil.copyfile(settings_file, new_settings)
    client = get_client(
        quiet=False,
        settings_file=new_settings,
    )
    return client


def get_updaters():
    client = get_client()
    return client.updaters
