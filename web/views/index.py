"""
index page
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import app_views

@app_views.route('/', methods=['GET'])
def index():
    return render_template("index.html")
