from flask import request, Blueprint, redirect, url_for, g

from github_integration import github, db
from github_integration.auth.utils import is_valid_github_token, \
    get_github_user
from github_integration.models import User

auth = Blueprint('auth', __name__)


@auth.route("/oauth/access_token", methods=["POST"])
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
        db.session.add(user)
        db.session.commit()
    return "", 200


@auth.route("/oauth")
def github_oauth():
    return github.authorize()


@auth.route('/oauth/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db.session.add(user)

    user.github_access_token = access_token

    # Not necessary to get these details here
    # but it helps humans to identify users easily.
    g.user = user
    github_user = github.get('/user')
    user.github_id = github_user['id']
    user.github_login = github_user['login']

    db.session.commit()

    db.session['user_id'] = user.id
    return redirect(next_url)


@auth.route('/logout')
def logout():
    db.session.pop('user_id', None)
    return redirect(url_for('/oauth'))

# @auth.route('/user')
# def user():
#     return jsonify(github.get('/user'))
