"""
forms init
"""
from wtforms import StringField, SubmitField, PasswordField, RadioField, SelectField, SelectMultipleField
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import DataRequired, Length

from web.forms.user import *
from web.forms.project import *
from web.forms.auth import *
