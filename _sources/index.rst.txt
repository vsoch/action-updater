.. _manual-main:

==============
Action Updater
==============

.. image:: https://img.shields.io/github/stars/vsoch/action-updater?style=social
    :alt: GitHub stars
    :target: https://github.com/vsoch/action-updater/stargazers

The actions updater will make it easy to update actions:

 - 🥑 updated syntax and commands
 - 🥑 versions of actions, either for releases or commits
 - 🥑 preview, write to new file, or write in place!

To see the code, head over to the `repository <https://github.com/vsoch/action-updater/>`_.


.. _main-getting-started:

---------------------------------------
Getting started with the Action Updater
---------------------------------------

There are two primary functions - to ``detect`` and ``update``!
The first previews changes to a workflow file (or directory) and the
second writes the changes to file.

.. code-block:: console

    $ action-updater detect .github/workfows/main.yaml
    $ action-updater update .github/workfows/main.yaml

And that's it! The action comes with several :ref:`getting_started_updaters` that will look
for particular aspects to lint or update. If you have a request for a new updated, please
`open an issue <https://github.com/vsoch/action-updater/issues>`_,

The Action Updater can be installed from pypi or directly from the repository. See :ref:`getting_started-installation` for
installation, and then the :ref:`getting-started` section for using the client.

.. _main-support:

-------
Support
-------

* For **bugs and feature requests**, please use the `issue tracker <https://github.com/vsoch/action-updater/issues>`_.
* For **contributions**, visit Caliper on `Github <https://github.com/vsoch/action-updater>`_.

---------
Resources
---------

`GitHub Repository <https://github.com/vsoch/action-updater>`_
    The code on GitHub.


.. toctree::
   :caption: Getting started
   :name: getting_started
   :hidden:
   :maxdepth: 2

   getting_started/index
   getting_started/user-guide
   getting_started/developer-guide

.. toctree::
    :caption: API Reference
    :name: api-reference
    :hidden:
    :maxdepth: 4

    source/modules
