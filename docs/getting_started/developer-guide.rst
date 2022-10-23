.. _getting_started-developer-guide:

===============
Developer Guide
===============

This developer guide includes more complex interactions like contributing
modular updaters. If you haven't read :ref:`getting_started-installation`
you should do that first.

.. _getting_started-developer-guide-linting:


Linting
=======

To lint your code, you can install pre-commit and other dependencies to your environment:

.. code-block:: console

    $ pip install -r .github/dev-requirements.txt


And run:

.. code-block:: console

    $ pre-commit run --all-files


Or install as a hook:

.. code-block:: console

    $ pre-commit install


.. _getting_started-developer-guide-developing-an-updater:


Developing an Updater
=====================

Each updater is required to have one file, ``update.py`` that uses the ``UpdaterBase`` class and
has one function to ``detect``. The easiest way to get this structure is to copy another updater completely,
and use it as a template.

Updater Class
-------------

Your updater class is discovered based on the module folder name. The class should be the uppercase of that,
with ``Updater`` as a suffix. E.g.,:

- setoutput -> SetoutputUpdater
- version -> VersionUpdater

If you don't follow this convention, we won't be able to discover it and use it! You'll also get errors
and know very quickly.

.. _getting_started-developer-guide-updater-metadata:

Updater Metadata
----------------

You are required to have:

- description
- name (typically same as the folder name, but not required) must be all lowercase and only ``-`` for special characters

Optionally, if you provide a schema (from `jsonschema <https://python-jsonschema.readthedocs.io/en/stable/>`_) and set to the schema attribute, this will validate
any user settings that your updater accepts. An example class definition is shown below:

.. code-block:: python

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


In the example above, notice we also have a "cache" that is used to store tags between runs.
We can do this because the updater is instantiated at the beginning of a run, and then the same
class used across workflow files. This means that if multiple files use ``actions/checkout``
(and thus the version updater needs to look up latest tags) we only do that once!

.. _getting_started-developer-guide-updater-settings:

Updater Settings
----------------

As shown above, when an updater defines a schema, this is matched to a block in settings.
If you want your settings to have defaults, add the nested block under ``updaters-><name>``. Here
is an example in ``action_updater/settings.yml`` for the schema above:

.. code-block:: yaml

    updaters:
      version:
        # Repository orgs to allow a major version (and not commit)
        major_orgs:
          - actions
          - docker

Since a developer user will likely be reading this file, it's recommended to put some comments to explain different fields.

.. _getting_started-developer-guide-updater-detect:


Updater Detect
--------------

Your updater class has a main function ``detect`` that must exist. Any and all other classes are largely optional (and of course encouraged to have a modular design)!
The function should expect an action (`action_updater.main.action.GitHubAction`) to be provided, and to look through the `action.jobs` and make any appropriate changes.
Here is a basic example. Note that we:

 - Keep track of self.count, setting it to 0 in the beginning, and incrementing it for each change.
 - Make changes directly to ``job.steps``. Since this is a copy of the original config, this is what will be changed (and saved to file, if desired).
 - Return a boolean to indicate if changes were detected.


.. code-block:: python

    def detect(self, action):
        """
        An example detection function
        """
        # Set the count to 0
        self.count = 0

        # No point if we don't have jobs!
        if not action.jobs:
            return False

        # For each job, look for steps->updater versions
        for job_name, job in action.jobs.items():

            # These are matched to steps
            for step in job.get("steps", []):

                # Get a "run" section
                run = step.get('run')

                # Get some new updated content
                # Perform checks for syntax, etc. here!
                updated_content = self.do_update(run)

                # Ensure to do a check to see if there are change
                if updated_content != step['run']:
                    self.count += 1
                    # To then update with changes:
                    step["run"] = updated_content

        return self.count != 0


The client will handle displaying changes and otherwise saving updates, so you do not need to
worry about that. The ``UpdaterClass`` also has several courtesy functions for gettings tags (``get_tags_lookup`` or ``get_tags``
along with releases (``get_releases``) and you can take advantage of them, or add additional API calls if needed to the base class.
The updater will also be automatically detected and registered, and included in basic testing, however you do need
to add a "before" and "after" set of yaml files, discussed next.

.. _getting_started-developer-guide-testing:

Testing
-------

Each updater should have a ``<name>-before.yaml`` and ``<name>-after.yaml`` in ``action_updater/tests/data``.
The format is simple - it should be a GitHub workflow (any of your choosing!) before and after running an update.
The easiest way to make this is to create a "before" file manually (with updates you know need to happen)
(in Python) create a client, run detect, and then write to an after file. And be sure to check that your
updater worked  as you would like! Here is an example (what I used for my test cases):


.. code-block:: python

    from action_updater.main import get_client
    cli = get_client()

    # Before and after files (assuming in present working directory)
    before_file = "save-state-before.yaml"
    after_file = "save-state-after.yaml"

    # Run detect *only* for the updater you care about
    action = cli.detect(before_file, updaters=['savestate'])

    # Write changes to new file (then check it!)
    action[before_file].write(after_file)

And then visually check it - and you should be done! These files will be used in testing,
along with testing basic output and metadata for your updater. If you have an idea for an updater but
don't have bandwidth to add? Please ping @vsoch by opening an issue!


.. _getting_started-developer-guide-updater-comments:

Updating Comments
-----------------

The ``action.jobs`` objects that you interact with are actually annotated with comments! If you want to update
them, I've found a good way to do this is to interact with the ``step.ca.items`` (or other json attribte).
Basically, this is a lookup of items (based on the key index) for which there is a list that corresponds to
the comment location. I found that what works is to define a new set of empty comments, and then to
use the provided function (by ruamel) to set one:

.. code-block:: python

    # Update the uses step with some new content
    step["uses"] = updated.strip()

    # Delete all locations of comments for it
    step.ca.items["uses"] = [None, None, None, None]

    # Add the "end of line" comment (the third one) - will add a CommentedToken
    step.yaml_add_eol_comment(f"# {comment}\n", "uses", column=0)


Note that you might want to do something more elegant (e.g., grab the previous comments in positions 0,1,3)
or whichever you want to preserve, to save before writing the new EOL comment.
You can look at the ``version`` updater for this full example. It is how we annotate the end
of the line with a new commented version.
