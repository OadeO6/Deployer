from . import (
    FlaskForm, StringField, SubmitField,
    DataRequired, PasswordField
)

class authForm(FlaskForm):
    name = StringField("Name", default="Annonymus...")
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
