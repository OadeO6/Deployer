"""
doc
"""
from flask import Blueprint, g, redirect, url_for, current_app
import functools
from web.views.images import UpdateSvg, SetingSvg, NewProjectSvg, ProfileSvg, ProjectsSvg

app_views = Blueprint("app_views", __name__, url_prefix="/")
auth_views = Blueprint("auth_views", __name__, url_prefix="/auth")
user_views = Blueprint("user_views", __name__, url_prefix="/user")

def need_login(view):
    @functools.wraps(view)
    def View(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth_views.login'))
        return view(*args, **kwargs)
    return View

def get_menus():
    return ([
        [
            "Profile",
            url_for("user_views.home"),
            ProfileSvg
        ],
        [
            "Projects",
            url_for("user_views.projects"),
            ProjectsSvg
        ],
        [
            "New Project",
            url_for("user_views.newProject"),
            NewProjectSvg
        ],
        [
            "Configurations",
            url_for("user_views.projects"),
            SetingSvg
        ],
        [
            "Update",
            url_for("user_views.projects"),
            UpdateSvg
        ]
    ])
from web.views.auth import *
from web.views.index import *
from web.views.dashboard import *
from web.views.project import *
from web.views.api import *
from web.views.dashboardextra import *
