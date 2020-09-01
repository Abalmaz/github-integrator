from flask import request, jsonify, Blueprint, \
    redirect, url_for, g, Response
from flask.views import MethodView

from src import github
from src.auth.constants import REQUIRED_SCOPES
from src.auth.utils import is_valid_github_token, \
    get_github_user, decode_personal_token
from src.auth.models import GitHubUser
from src.database import db_session

auth = Blueprint('auth', __name__)


class PersonalTokenAuth(MethodView):
    """
    Connect with personal token to GitHub.
    If the user's github token is valid we authorized him.
    """

    def post(self) -> Response:
        post_data = request.get_json()
        try:
            github_personal_token = post_data.get('personal_token')
            if not is_valid_github_token(github_personal_token):
                response_object = {
                    'status': 'fail',
                    'message': 'Token is not valid'
                }
                return jsonify(response_object)
            return redirect(
                url_for('auth.authorized_personal_token',
                        access_token=github_personal_token
                        )
            )
        except Exception:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return jsonify(response_object)


class AuthorizedPersonalToken(MethodView):
    """
    Authorized user.
    """

    def get(self,
            access_token: str
            ) -> Response:
        github_token = request.args.get('access_token')
        if github_token is None:
            return jsonify({
                'status': 'fail',
                'message': 'Token is not define'
            })
        return save_github_user(github_token)


class GitHubAppAuth(MethodView):
    """
    View allows you authenticate your users via
    GitHub App using OAuth protocol.
    """

    def get(self) -> Response:
        github.authorize(scope=list(REQUIRED_SCOPES))
        return github.authorize()


@auth.route('/oauth/github-callback')
@github.authorized_handler
def authorized(access_token: str) -> Response:
    return save_github_user(access_token)


def save_github_user(token: str) -> Response:
    try:
        github_user = get_github_user(token)
        print(f"Github user: {github_user}")
        user = GitHubUser.query.filter_by(
            github_id=github_user['id']
                ).first()
        if user and decode_personal_token(user.github_access_token) == token:
            g.user = user
        else:
            user = GitHubUser(github_access_token=token,
                              github_email=github_user['email'],
                              github_id=github_user['id'],
                              github_login=github_user['login'])
            db_session.add(user)
            db_session.commit()
        response_object = {'status': 'success',
                           'message': 'Successfully authorized user.'
                           }
        return jsonify(response_object)
    except Exception:
        response_object = {"status": "fail",
                           "message": "GitHub user didn't find"
                           }
        return jsonify(response_object)


# define the API resources
personal_token_auth_view = PersonalTokenAuth.as_view(
    'personal_token_auth'
)
authorized_view = github.authorized_handler(
    AuthorizedPersonalToken.as_view('authorized_personal_token')
)

github_app_auth_view = GitHubAppAuth.as_view('github_app_auth')

# add Rules for API Endpoints
auth.add_url_rule('/oauth/access_token',
                  view_func=personal_token_auth_view,
                  methods=['POST']
                  )
auth.add_url_rule('/oauth/personal-token-callback',
                  view_func=authorized_view,
                  methods=['GET']
                  )
auth.add_url_rule('/oauth',
                  view_func=github_app_auth_view
                  )
