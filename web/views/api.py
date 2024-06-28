"""
authentications
"""
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth_views

@auth_views.route('/doc/api', methods=['GET'])
def api():
    render_template("api.html")
