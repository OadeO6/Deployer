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
from web.views.images import PlusSvg, LoadingSvg


@user_views.route('/db/del/<string:id>', methods=['POST', 'GET'])
@user_views.route('/db/del/mul', methods=['POST'])
@need_login
def deleteDb(id="mul"):
    if id == "mul":
        if request.method == 'GET':
            return redirect(url_for("user_views.dbServers"))
        data = request.get_json()

        if not data or 'itemIds' not in data:
            flash("Something Whent Wrong", "error")
            return redirect(url_for("user_views.dbServers"))

        item_ids = data['itemIds']

        if not isinstance(item_ids, list) or not item_ids:
            flash("Something Whent Wrong", "error")
            return redirect(url_for("user_views.dbServers"))
        res =  redirect(url_for("user_views.dbServers"))
    else:
        item_ids = [id]
        res = redirect(url_for("user_views.dbServers"))


    success = DBServer.Delete(item_ids)
    print("dell00000000", item_ids)
    if success:
        flash("Deleted Project Successfully", "success")
    else:
        flash("Something Whent Wrong", "error")
    return res

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
                build_id = project_id["build_id"]
                project_id = project_id["id"]
            else:
                flash("No Relative project found defaulting to global DB server",
                      "warning")
                project_id = None
                build_id = None
        else:
            project_id = None
            build_id = None
        dataBase = DBServer(session.get("user_id"), project_id, form, build_id)
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
        databases = dbserver[0]
    else:
        return abort(404)
    builds = DBServer.getbuilds(id=id)
    return render_template(
        "dbServer.html",
        apiUrl= 'http://localhost:5000/user/database/api1',
        curentUrl=url_for("user_views.dbServer", id=id),
        menubar=get_menus(), id=id,
        build=builds[0] if len(builds) > 0 else {},
        databases=databases
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
        LoadingSvg = LoadingSvg,
        projects=dbservers,
        PlusSvg = PlusSvg
    )


@user_views.route('/database/api1', methods=['POST'])
def query():
    import os

    data = request.get_json()
    print(data)
    query = data["query"]
    type = data["type"]
    url = data["url"]
    paswd = data["pass"]
    user = data["user"]
    database = data["dbname"]
    remote_host, port_number = url.split(":")
    if type.lower() == "mongodb":
        command = f"""sudo docker run --rm --network host mongo:3.6.13-xenial mongo --host '{remote_host}' --port '{port_number}' {database} --password '{paswd}' --username '{user}' --eval '{ query }' --quiet
        """
    elif type.lower() == "mysqli":
        command = f"""sudo docker
        mysql -h {remote_host} -P {port_number} -u {user} -p{paswd} -D {database} -e " { query} ;"
        """
    else:
        command = "echo Error"
    print(command)
    result = os.popen(command).read()
    return jsonify({ "result": result })
