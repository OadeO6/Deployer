from . import FlaskForm, StringField, SubmitField, RadioField, SelectField, SelectMultipleField

class projectForm(FlaskForm):
    mode = RadioField(default="dev", choices=["ade","dev"])
    projectName = StringField("Project Name")
    repoUrl = StringField("Repo Url", default="https://github.com/Ade06AA/mytest")
    envKey = StringField("Key")
    envValue = StringField("Value")
    projectType = SelectField("Select an option", choices=[("Next", "Next"), ("Flask", "Flask")])
    projectdirectory = StringField("Project Directory")
    hostIp = StringField("Custom Host Ip")
    buildCommand = StringField("Build Command")
    installCommand = StringField("Install Command")
    deployCommans = StringField("Deploy Command")
    webServer = SelectField("Web Server")
    dataBaseServer = SelectMultipleField("Select servers", default=["a","b"], choices=["a", "b", "c"])
    """
    dataBaseServer = SelectMultipleField("Select servers", choices=[
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("AE", "AE"), ("OLA", "OLA"),
        ("AD", "AD"), ("BOL", "BOL")
    ])
    """
    submit = SubmitField("Next")
