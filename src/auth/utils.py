import requests
from flask import Response

from src import encryption_type
from src.auth.constants import REQUIRED_SCOPES


class GitHubError(Exception):
    """Raised if a request fails to the GitHub API."""

    def __str__(self):
        try:
            message = self.response.json()['message']
        except Exception:
            message = None
        return f'{self.response.status_code} {message}'

    @property
    def response(self) -> Response:
        """The :class:`~requests.Response` object for the request."""
        return self.args[0]


def is_valid_response(response: Response) -> bool:
    """
    Check response status, return True if
    the request was successfully received,
    understood, and accepted
    """
    return 200 <= response.status_code <= 299


def is_json_response(response: Response) -> bool:
    content_type = response.headers.get('Content-Type', '')
    return content_type == 'application/json' or content_type.startswith(
        'application/json;'
    )


def is_set_includes_all_from_another(first_set: set,
                                     second_set: set
                                     ) -> bool:
    """
    Compare two sets, and if they are identical, return True
    """
    return True if len(
        list(set(first_set) & set(second_set))
    ) == 5 else False


def is_valid_github_token(personal_token: str) -> bool:
    """
    Check user's token, is it valid and have right scopes
    """
    url = 'https://api.github.com'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + personal_token
    }
    response = requests.request("GET", url, headers=headers)
    if is_valid_response(response):
        scopes = response.headers.get('X-OAuth-Scopes')
        user_scopes = set(scopes.split(', '))
        if is_set_includes_all_from_another(user_scopes,
                                            REQUIRED_SCOPES):
            return True
    return False


def get_github_user(user_token: str) -> Response:
    """
    Get information about GitHub user
    """
    url = 'https://api.github.com/user'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + user_token
    }
    response = requests.request("GET", url, headers=headers)

    if not is_valid_response(response):
        raise GitHubError(response)

    if is_json_response(response):
        return response.json()


def encrypt_personal_token(personal_token: str) -> str:
    """
    Function for encrypting, using Ferner library
    """
    return encryption_type.encrypt(
        personal_token.encode()
    ).decode()


def decode_personal_token(personal_token: str) -> str:
    """
    Function for decrypting, using Ferner library
    """
    return encryption_type.decrypt(
        personal_token.encode()
    ).decode()
