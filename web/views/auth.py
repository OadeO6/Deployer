"""
authentications
"""
from pymongo import errors
from models.user import User
from urllib.parse import urlparse
from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from web.forms import authForm
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth_views

users = [{"email":"email", "name": "ade", "age": 20, "user_id":"userid"}]

def get_temp(val, key):
    return [x if x.get(key) == val else None for x in users][0]

@auth_views.before_app_request
def setUpA():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #g.user = get_temp(user_id, "user_id")
        # use redis to handle user session
        g.user = session.get("user_name")


@auth_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = False
        if not password:
            flash("Password field is required")
            error= True
        if not email:
            flash("Email fiel is required")
            error= True

        # find the user
        user = User.find({"email": email}, {"name": 1, "id": 1, "password": 1})
        if user:
            user = user[0]
        #user = get_temp(email, "email") if not error else None
        if user:
            print(user)
            #session["user_id"] = user["user_id"] # temp ............ .
            if check_password_hash(user.get("password"), password):
                error = False
                session["user_id"] = user.get("id") # temp ............ .
                session["user_name"] = user.get("name") # temp ............ .
            else:
                flash("Incorrect cridentials")
                error = True
        else:
            flash("Incorrect cridentials")
            error= True
        if not error:
            temp = session.get("thePrevious_url")
            return redirect(temp if temp is not None else url_for('app_views.index'))
    form = authForm()
    back = request.referrer
    if back:
        #if back not in [url_for('auth_views.register'), url_for('auth_views.register')]:
        back = urlparse(request.referrer).path
        if back not in [url_for('auth_views.login'), url_for('auth_views.register')]:
            session['thePrevious_url'] = back
    return render_template("login.html", form=form)

@auth_views.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('app_views.index'))

@auth_views.route('/signin', methods=['GET', 'POST'])
def register():
    form = authForm()
    if request.method == "POST":
        error = False
        name = form.name.data
        email = request.form['email']
        password = request.form['password']
        if not password:
            flash("Password field is required")
            error= True
        if not email:
            flash("Email fiel is required")
            error= True
        if not error:
            # add user to database
            user = User(name, email, generate_password_hash(password))
            try:
                user.save()
            except errors.DuplicateKeyError as e:
                flash("Email already exist")
                return render_template("signin.html", form=form)

            return redirect(url_for('auth_views.login'))
    form = authForm()
    return render_template("signin.html", form=form)
