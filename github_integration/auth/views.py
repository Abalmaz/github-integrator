from flask import request, make_response, jsonify, Blueprint, \
    redirect, url_for, g
from flask.views import MethodView

from github_integration import db, github
from github_integration.auth.constants import REQUIRED_SCOPES
from github_integration.auth.utils import is_valid_github_token, \
    get_github_user
from github_integration.auth.models import GitHubUser
from github_integration.auth.utils import encrypt_personal_token


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
            print("Personal token: {github_personal_token}")
            print(github_personal_token)
            if is_valid_github_token(github_personal_token):
                return redirect(
                    url_for('auth.authorized',
                            access_token=github_personal_token
                            )
                )
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


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
    def get(self, access_token):
        github_token = request.args.get('access_token')
        if github_token is None:
            return 'Token is not define', 200
        encrypt_github_personal_token = encrypt_personal_token(
            github_token
        )
        user = GitHubUser.query.filter_by(
            github_access_token=encrypt_github_personal_token
        ).first()
        if user is None:
            user = GitHubUser(encrypt_github_personal_token)
            db.session.add(user)
        g.user = user
        github_user = get_github_user(github_token)
        user.github_id = github_user['id']
        user.github_login = github_user['login']
        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Successfully authorized user.'
        }
        return make_response(jsonify(responseObject)), 201


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
