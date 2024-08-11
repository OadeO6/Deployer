from wtforms import FieldList, FormField
from . import FlaskForm, StringField, SubmitField, RadioField, SelectField, SelectMultipleField

class test(FlaskForm):
    name = StringField('')
class projectForm(FlaskForm):

    name = StringField('', render_kw={'readonly': True})
    items = FieldList(name, min_entries=1)

    mode = RadioField("Deployment Mode", default="dev", choices=[("pro", "Production"), ("dev", "Development")])
    stage = RadioField("", default="full", choices=["full", "pre", "post"])
    projectName = StringField("Project Name")
    deployOrNot = RadioField("deployOrNot",
                             default= "deploy",
                             choices=[
                             ("notDeploy", "create project witout deploying"),
                             ("deploy" ,"create and deploy")
                             ])
    repoUrl = StringField("Repository URL") #, default="https://github.com/Ade06AA/mytest")
    envKey = StringField("Key")
    envValue = StringField("Value")
    projectType = SelectField("Select an option", choices=[("Flask", "Flask"), ("Django", "Django"), ("Next", "Next"), ("React", "React"), ("Python", "Python"), ("JavaScript", "JavaScript"), ("Node", "Node")])
    projectDirectory = StringField("Project Directory")
    hostIp = StringField("Custom Host Ip")
    buildCommand = StringField("Build Command")
    installCommand = StringField("Install Command")

    deployCommand = StringField("Deploy Command")




    webServer = SelectField("HTTP Server", choices=[("Gunicorn", "Gunicorn"), ("uWSGI", "uWSGI")])
    """
    dataBaseServer = SelectMultipleField("Select servers", choices=[
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("AE", "AE"), ("OLA", "OLA"),
        ("AD", "AD"), ("BOL", "BOL")
    ])

    """
    submit = SubmitField("Deploy Project")
