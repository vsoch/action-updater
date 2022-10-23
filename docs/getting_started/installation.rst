.. _getting_started-installation:

============
Installation
============

The Action Updater can be installed from pypi, or from source.




Pypi
====

The module is available in pypi as `action-updater <https://pypi.org/project/singularity-hpc/>`_,
and to install we first recommend some kind of virtual environment:

.. code-block:: console

    $ python -m venv env
    $ source env/bin/activate

And then install from pypi using pip:

.. code-block:: console

    $ pip install action-updater

You can also clone the repository (branch or release) and install from that.


Repository
==========

To install from source, again starting with a virtual environment:



.. code-block:: console

    $ python -m venv env
    $ source env/bin/activate

You'll want to clone (or download a .tar.gz release) and then install:

.. code-block:: console

    $ git clone https://github.com/vsoch/action-updater
    $ cd action-updater
    $ pip install -e . # development mode
    $ pip install .    # to your python install

Next head over to :ref:`getting-started` to get started using the action updater!
