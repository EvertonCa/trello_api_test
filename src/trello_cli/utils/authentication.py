import sys
from os import environ
from enum import Enum

from .exceptions import EnvVarException


class TrelloEnvVars(Enum):
    """
    Trello's authentication variables to be searched in the user's environment
    """
    API_KEY = "TRELLO_API_KEY"
    API_TOKEN = "TRELLO_API_TOKEN"


class TrelloAuthenticationFromEnv:
    """
    Retrieves from the user environment variables the necessary authentication for Trello
    """
    def __init__(self) -> None:

        # checks for the necessary authentication environment variables
        try:
            self._validate_vars()
        except EnvVarException as e:
            print(f"[AUTHENTICATION ERROR] {e}")
            sys.exit(-1)

        # authentication
        self.API_KEY = environ[TrelloEnvVars.API_KEY.value]
        self.API_TOKEN = environ[TrelloEnvVars.API_TOKEN.value]

    @staticmethod
    def _validate_vars() -> None:
        """
        Checks if the necessary authentication variables do exist in the user's environment.
        """
        authentication_vars = [x.value for x in TrelloEnvVars]
        missing_vars = []
        for varname in authentication_vars:
            if varname not in environ or len(environ[varname]) == 0:
                missing_vars.append(varname)

        if len(missing_vars) > 0:
            raise EnvVarException(missing_vars)
