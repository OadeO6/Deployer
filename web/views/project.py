"""
authentications
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, jsonify
)
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
    return render_template("newproject.html", form=form, curentUrl=url_for("user_views.newProject"), menubar=get_menus())

@user_views.route('/project/<string:id>', methods=['GET'])
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
        curentUrl=url_for("user_views.projects", id=id),
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
    # make output a render_template object instaed
    return jsonify({
        "output": render_template("projectOutPut.html", data=output),
        "building": building})
