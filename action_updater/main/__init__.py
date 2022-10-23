__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


from .settings import Settings


def get_client(quiet=False, **kwargs):
    """
    Get an actions updater client.

    This will ensure we add all of the default updaters to our client.
    """
    # TODO we can further customize here.
    validate = kwargs.get("validate", True)

    # Load user settings to add to client, and container technology
    settings = Settings(kwargs.get("settings_file"), validate)

    from .client import ActionUpdater

    ActionUpdater.settings = settings
    client = ActionUpdater(**kwargs, quiet=quiet)
    return client
