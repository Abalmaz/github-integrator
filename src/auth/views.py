from flask import request, make_response, jsonify, Blueprint, \
    redirect, url_for, g
from flask.views import MethodView

from src import db, github
from src.auth.constants import REQUIRED_SCOPES
from src.auth.utils import is_valid_github_token, \
    get_github_user
from src.auth.models import GitHubUser


auth = Blueprint('auth', __name__)


class PersonalTokenAuth(MethodView):
    """
    Connect with personal token to GitHub.
    If the user's github token is valid we authorized him.
    """
    def post(self):
        post_data = request.get_json()
        try:
            github_personal_token = post_data.get('personal_token')
            if not is_valid_github_token(github_personal_token):
                response_object = {
                    'status': 'fail',
                    'message': 'Token is not valid'
                }
                return make_response(
                    jsonify(response_object)
                ), 500
            github_user = get_github_user(github_personal_token)
            return redirect(
                url_for('auth.authorized',
                        access_token=github_personal_token,
                        github_user_id=github_user['id']
                        )
            )
        except Exception:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(
                jsonify(response_object)
            ), 500


class GitHubAppAuth(MethodView):
    """
    View allows you authenticate your users via
    GitHub App using OAuth protocol.
    """
    def get(self):
        github.authorize(scope=list(REQUIRED_SCOPES))
        return github.authorize()


class Authorized(MethodView):
    """
    Authorized user.
    """
    def get(self, access_token, github_user_id=None):
        user = None
        github_token = request.args.get('access_token')
        github_user_id = request.args.get('github_user_id')
        if github_token is None:
            return 'Token is not define', 200
        if github_user_id:
            user = GitHubUser.query.filter_by(
                github_id=github_user_id
            ).first()
        if not user:
            user = GitHubUser(github_token)
            db.session.add(user)
        g.user = user
        github_user = get_github_user(github_token)
        if github_user:
            user.github_id = github_user['id']
            user.github_login = github_user['login']
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully authorized user.'
            }
            return make_response(
                jsonify(response_object)
            ), 201

        return "GitHub user didn't find"


# define the API resources
personal_token_auth_view = PersonalTokenAuth.as_view(
    'personal_token_auth'
)
authorized_view = github.authorized_handler(
    Authorized.as_view('authorized')
)
github_app_auth_view = GitHubAppAuth.as_view('github_app_auth')

# add Rules for API Endpoints
auth.add_url_rule('/oauth/access_token',
                  view_func=personal_token_auth_view,
                  methods=['POST']
                  )
auth.add_url_rule('/oauth/github-callback',
                  view_func=authorized_view,
                  methods=['GET']
                  )
auth.add_url_rule('/oauth',
                  view_func=github_app_auth_view
                  )
