import requests
from flask import abort, Response

from github_integration.auth.constance import REQUIRED_SCOPES


class GitHubError(Exception):
    """Raised if a request fails to the GitHub API."""

    def __str__(self):
        try:
            message = self.response.json()['message']
        except Exception:
            message = None
        return "%s: %s" % (self.response.status_code, message)

    @property
    def response(self):
        """The :class:`~requests.Response` object for the request."""
        return self.args[0]


def is_valid_response(response):
    return 200 <= response.status_code <= 299


def is_json_response(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type == 'application/json' \
           or content_type.startswith('application/json;')


def is_set_includes_all_from_another(first_set, second_set):
    return False if second_set - first_set else True


def is_valid_github_token(personal_token):
    url = 'https://api.github.com'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + personal_token
    }
    response = requests.request("GET", url, headers=headers)
    if is_valid_response(response):
        return True
        # scopes = response.headers.get('X-OAuth-Scopes')
        # user_scopes = set(scopes.split(', '))
        # if is_set_includes_all_from_another(user_scopes, REQUIRED_SCOPES):
        #     return True
        # else:
        #     abort(Response("Token doesn't have enough scopes"))
    else:
        abort(Response("Token is not valid"))
    return False


def get_github_user(user_token):
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
