from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix='/api/v!')
auth_views = Blueprint("auth_views", __name__, url_prefix='/api/v!/auth')

from api.v1.views.auth.auth import *
