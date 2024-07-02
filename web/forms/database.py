from . import FlaskForm, StringField, SubmitField, RadioField, SelectField, SelectMultipleField

class dataBaseForm(FlaskForm):
    # mode = RadioField(default="dev", choices=["ade","dev"])
    # projectName = StringField("Project Name")
    # repoUrl = StringField("Repo Url", default="https://github.com/Ade06AA/mytest")
    # envKey = StringField("Key")
    # envValue = StringField("Value")
    # projectType = SelectField("Select an option", choices=[("Next", "Next"), ("Flask", "Flask")])
    # projectdirectory = StringField("Project Directory")
    # hostIp = StringField("Custom Host Ip")
    # buildCommand = StringField("Build Command")
    # installCommand = StringField("Install Command")
    # deployCommand = StringField("Deploy Command")
    # webServer = SelectField("Web Server")
    # dataBaseServer = SelectMultipleField("Select servers", default=["a","b"], choices=["a", "b", "c"])
    dataBaseName = StringField("Name")
    dataBasetype = SelectField("Select an option", choices=[("Mongo Db", "MongoDb"), ("Mysql", "Mysql")])
    dataBaseUserName = SelectField("User name")
    dataBasePassword = SelectField("User password")
    """
    dataBaseServer = SelectMultipleField("Select servers", choices=[
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("ADE", "ADE"), ("BOLA", "BOLA"),
        ("AE", "AE"), ("OLA", "OLA"),
        ("AD", "AD"), ("BOL", "BOL")
    ])
    """
    submit = SubmitField("Create Data-base")
