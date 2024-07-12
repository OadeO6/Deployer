"""
database
"""
from flask import (
    flash, g, request, redirect, render_template, request, session, url_for, abort, jsonify
)
# from jenkins import requests
# from six.moves import urllib
from web.forms.database import dbServerForm
from models.database import DBServer
from models.project import Project
from . import user_views, need_login, get_menus
from web.views.images import PlusSvg


@user_views.route('/dbserver/new', methods=['GET', 'POST'])
@need_login
def newDBServer():
    """
    creata a data base
    """
    form = dbServerForm()
    if request.method == "POST":
        if form.dataBaseScope.data == "local":
            project_id = Project.find({"name": form.dbProjectName.data})
            if len(project_id) == 1:
                project_id = project_id[0]
            else:
                flash("No Relative project found defaulting to global DB server",
                      "warning")
                project_id = None
        else:
            project_id = None
        dataBase = DBServer(session.get("user_id"), project_id, form)
        dataBase.build()
        dataBase.save()
    return render_template("newDBServer.html", form=form,
                           curentUrl=url_for("user_views.newDBServer"),
                           menubar=get_menus())

@user_views.route('/dbserver/<string:id>', methods=['GET'])
@need_login
def dbServer(id):
    dbserver = DBServer.find({"id":id})
    if dbserver:
        dbserver = dbserver[0]
    else:
        return abort(404)
    databases = dbserver.data_bases
    return render_template(
        "dbServer.html",
        curentUrl=url_for("user_views.dbServer", id=id),
        menubar=get_menus(), id=id, databases=databases
    )

@user_views.route('/dbservers', methods=['GET'])
@need_login
def dbServers():
    dbservers = DBServer.find({"user_id": session.get("user_id")})
    # print(projects)
    # for project in projects:
    #     print(project)
    #     Data = Build.find({"project_id": project["id"]})
    #     print(Data)
    #     if len(Data) == 1:
    #         Data = Data[0]
    #     else:
    #         Data = {}
    #     project["building"] = Data.get("building", False)
    #     project["status"] = Data.get("status", None)
    return render_template(
        "dbServers.html",
        curentUrl=url_for("user_views.dbServers"),
        menubar=get_menus(),
        projects=dbservers,
        PlusSvg = PlusSvg
    )
