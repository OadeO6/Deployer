"""
projects
"""
from flask import (
    Blueprint, flash, g, request, redirect, render_template, request, session, url_for, abort, jsonify
)
from jenkins import requests
from six.moves import urllib
from werkzeug.security import check_password_hash, generate_password_hash
from web.forms import projectForm
from models.project import Project
from models.build import Build
from . import user_views, need_login, get_menus

@user_views.route('/projects', methods=['GET'])
@need_login
def projects():
    projects = Project.find({"user_id": session.get("user_id")})
    print(projects)
    for project in projects:
        print(project)
        Data = Build.find({"project_id": project["id"]})
        print(Data)
        if len(Data) == 1:
            Data = Data[0]
        else:
            Data = {}
        project["building"] = Data.get("building", False)
        project["status"] = Data.get("status", None)
    return render_template(
        "projects.html",
        curentUrl=url_for("user_views.projects"),
        menubar=get_menus(),
        projects=projects
    )

# @user_views.route('/project/new', methods=['GET', 'POST'])
# @user_views.route('/project/new/<string:id>', methods=['POST'])
# @need_login
# def newProject(id=None): # old newProject
#     form = projectForm()
#     if request.method == "POST":
#     #if form.validate_on_submit():
#         #return redirect(url_for("user_views.newproject"))
#         """
#         projectName = form.projectName.data
#         repoUrl = request.form["repoUrl"]
#         envKey = request.form["envKey"]
#         envValue = request.form["envValue"]
#         projectType = request.form["projectType"]
#         projectdirectory = request.form["projectdirectory"]
#         hostIp = request.form["hostIp"]
#         buildCommand = request.form["buildCommand"]
#         installCommand = request.form["installCommand"]
#         deployCommans = request.form["deployCommans"]
#         """
#         if id:
#             project = Project(session.get("user_id"), _id=id)
#             project.rebuild()
#         else:
#             project = Project(session.get("user_id"), form)
#             project.build()
#         project.save()
#         return redirect(url_for("user_views.project", id=project.id))
#     #form = {"submit":2}
#     return render_template("newproject.html", form=form, curentUrl=url_for("user_views.newProject"), menubar=get_menus())

# @user_views.route('/database/new', methods=['GET', 'POST'])
# @need_login
# def newDataBase():
#     """
#     creata a data base
#     """
#     form = dataBaseForm()
#     if request.method == "POST":
#         dataBase = DataBase(session.get("user_id"), form)
#         dataBase.build()
#         dataBase.save()
#     return render_template("newDataBase.html", form=form, curentUrl=url_for("user_views.newDataBase"), menubar=get_menus())
#
# @user_views.route('/database/<string:id>', methods=['GET'])
# @need_login
# def dataBase(id):
#     dataBase = DataBase.find({"id":id})
#     if dataBase:
#         dataBase = dataBase[0]
#     else:
#         return abort(404)
#     builds = Project.getbuilds(id=id)
#     curentBuild = Project.getCurentBuild(id, project["current_build_num"])
#     return render_template(
#         "dataBase.html",
#         curentUrl=url_for("user_views.dataBase", id=id),
#         menubar=get_menus(), id=id
#     )
#
# @user_views.route('/databases', methods=['GET'])
# @need_login
# def dataBases():
#     dataBases = DataBase.find({"user_id": session.get("user_id")})
#     # print(projects)
#     # for project in projects:
#     #     print(project)
#     #     Data = Build.find({"project_id": project["id"]})
#     #     print(Data)
#     #     if len(Data) == 1:
#     #         Data = Data[0]
#     #     else:
#     #         Data = {}
#     #     project["building"] = Data.get("building", False)
#     #     project["status"] = Data.get("status", None)
#     return render_template(
#         "dataBases.html",
#         curentUrl=url_for("user_views.dataBases"),
#         menubar=get_menus(),
#         projects=dataBases
#     )



@user_views.route('/project/new', methods=['GET', 'POST'])
@user_views.route('/project/new/<string:id>', methods=['POST'])
@need_login
def newProject(id=None):
    form = projectForm()
    if request.method == "POST":
    #if form.validate_on_submit():
        #return redirect(url_for("user_views.newproject"))
        """
        projectName = form.projectName.data
        repoUrl = request.form["repoUrl"]
        envKey = request.form["envKey"]
        envValue = request.form["envValue"]
        projectType = request.form["projectType"]
        projectdirectory = request.form["projectdirectory"]
        hostIp = request.form["hostIp"]
        buildCommand = request.form["buildCommand"]
        installCommand = request.form["installCommand"]
        deployCommans = request.form["deployCommans"]
        """
        if id:
            project = Project(session.get("user_id"), _id=id)
            project.rebuild()
        else:
            project = Project(session.get("user_id"), form)
            project.build()
        project.save()
        return redirect(url_for("user_views.project", id=project.id))
    #form = {"submit":2}
    return render_template("newProject.html",
                           form=form,
                           apiUrl= 'http://localhost:5000/user/project',
                           curentUrl=url_for("user_views.newProject"),
                           menubar=get_menus())

@user_views.route('/project/<string:id>', methods=['GET'])
@need_login
def project(id):
    project = Project.find({"id":id})
    if project:
        project = project[0]
    else:
        return abort(404)
    builds = Project.getbuilds(id=id)
    curentBuild = Project.getCurentBuild(id, project["current_build_num"])
    return render_template(
        "project.html",
        curentUrl=url_for("user_views.project", id=id),
        menubar=get_menus(), project=project,
        builds=builds, build=curentBuild, id=id
    )

# to be moved to the main api
# because of how frequently request is sent here
@user_views.route('/project/<string:id>/api1', methods=['GET'])
def projectApi(id):
    print("yhhhhh")
    project = Project.find({"id":id})
    if project:
        project = project[0]
    else:
        return abort(404)
    BuildData = Project.getBuildData(project["build_id"], project["current_build_num"])
    building = BuildData["building"]
    output = BuildData["output"]
    l1 = []
    l2 = [None, None]
    output = [a for a in output.split('\n') if "[Pipeline]" not in a]
    skip = 0
    length = len(output)
    for i in range(length):
        if skip:
            skip -= 1
            continue
        _line: str = output[i]
        if _line.startswith('+ '):
            l2 = [None, None]
            if '@show1@' in _line:
                l2 = [_line.split("@show1@")[-1], None]
                l1.append(l2)
                print(l2)
            elif "@show2@" in _line:
                l2 = [_line.split("@show2@")[-1], ""]
                l1.append(l2)
                skip = 2 # skip next two lines
                print(l2)
        elif l2[1] != None:
            l2[1] = f"{l2[1]}\n{_line}"

    output = l1
    print(l1)
    # make output a render_template object instaed
    return jsonify({
        "output": render_template("projectOutPut.html", data=output),
        "building": building})

@user_views.route('/project/<string:name>/api4', methods=['GET'])
def checkApi(name):
    res = Project.find({"name": name})
    if len(res) != 0:
        data = False
    else:
        data = True
    return jsonify({ "data": data })

@user_views.route('/project/api5/api5', methods=['POST'])
def checkRepo():
    resdata = request.get_json()
    repo = urllib.parse.unquote(resdata.get('repo_url'))
    main_repo = repo.replace("http://github.com/", "")
    main_repo = repo.replace("https://github.com/", "")
    try:
        token_start = repo.find('://') + 3
        token_end = repo.find('@')
        token = repo.find('@')
        token = repo[token_start:token_end]
        api_url = repo.replace(token + '@', '').replace('.git', '')

        headers = {'Authorization': f'token {token}'}

        main_repo = api_url.replace("http:/github.com/", "")
        main_repo = api_url.replace("https://github.com/", "")
        print("main_repo", main_repo)
        response = requests.get(f'https://api.github.com/repos/{main_repo}', headers=headers)
        print("code", response.status_code)
        assert  response.status_code == 200, "No such repo"
        data = True
    except Exception as e:
        print(e)
        try:
            response = requests.get(f'https://api.github.com/repos/{main_repo}')
            assert  response.status_code == 200, "No such repo"
            data = True
        except Exception as e:
            print("2sss",e)
            data = False
    return jsonify({ "data": data })

@user_views.route('/project/<string:pType>/api3', methods=['GET'])
def createProjectApi(pType):
    pType = pType.lower()
    form = projectForm()
    if pType == "flask":
        data = render_template("projectFlask.html", form=form)
    elif pType == "next":
        data = render_template("projectNext.html", form=form)
    else:
        data = None
    return jsonify({ "data": data })

@user_views.route('/project/<string:_id>/<int:num>/api2', methods=['PUT'])
def updateBuildStatus(_id, num):
    """
    endpoint to update build status after jenkins is done with build
    """
    print(_id, num)
    try:
        Build.updateBuildStat({"id": _id, "build_num": num}, "jenkins")
    except Exception as e:
        raise e
    return jsonify({})
