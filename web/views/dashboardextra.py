"""
authentications
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import user_views, get_menus, need_login

@user_views.route('/seting', methods=['GET', 'POST'])
@need_login
def segting():
    return render_template("seting.html", urentUrl=url_for('user_views.home'), menubar=get_menus())


@user_views.route('/update', methods=['GET', 'POST'])
@need_login
def update():
    return render_template("seting.html", urentUrl=url_for('user_views.home'), menubar=get_menus())
