"""
authentications
"""
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import user_views, need_login, get_menus



@user_views.route('/home', methods=['GET'])
@need_login
def home():
    return render_template("dashboard.html", curentUrl=url_for('user_views.home'), menubar=get_menus())
