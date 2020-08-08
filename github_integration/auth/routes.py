from flask import render_template, request, Blueprint, jsonify, redirect

from github_integration.auth.utils import is_valid_github_token, get_github_user
from github_integration.models import User

auth = Blueprint('auth', __name__)


@auth.route("/auth/personal_token", methods=["POST"])
def personal_token_auth():
    post_data = request.get_json(force=True)
    personal_token = post_data['personal_token']
    if is_valid_github_token(personal_token):
        user = get_github_user(personal_token)
        user_github_id = user['id']
        user_github_login = user['login']
        user = User(github_access_token=personal_token,
                    github_id=user_github_id,
                    github_login=user_github_login)
        user.save()
    return "", 200
