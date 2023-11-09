class EnvVarException(Exception):
    """
    Raised when the necessary environment variables are absent or empty.
    """

    def __init__(self, envvars: str | list[str]) -> None:
        if isinstance(envvars, str):
            envvars = [envvars]
        self.vars = envvars
        super().__init__(
            f"The following environment authentication variables were empty or not found: {', '.join(envvars)}.")


class ListNotFoundException(Exception):
    """
    Raised when the requested list could not be found.
    """

    def __init__(self, list_name: str) -> None:
        super().__init__(f"The following list could not be found in Trello: {list_name}.")


class LabelNotFoundException(Exception):
    """
    Raised when the requested label could not be found.
    """

    def __init__(self, label_name: str) -> None:
        super().__init__(f"The following label could not be found in Trello: {label_name}.")


class APIRequestException(Exception):
    """
    Raised when an API exception occur.
    """

    def __init__(self, error: str) -> None:
        super().__init__(f"An error occurred while communicating with Trello's API: {error}.")
