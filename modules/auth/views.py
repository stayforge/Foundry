"""
   Login, Logout and register, callback
"""
import os
from urllib.parse import urlencode

from flask import Blueprint, url_for, session, redirect

from main import oauth

auth = Blueprint('auth', __name__,
                 template_folder='templates',
                 static_folder='static',
                 url_prefix='/auth/')


@auth.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@auth.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            }
        )
    )
