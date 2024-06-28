from . import FlaskForm, StringField, SubmitField

class UNameForm(FlaskForm):
    name = StringField("eg: ADE")
    submit = SubmitField("Submit")
