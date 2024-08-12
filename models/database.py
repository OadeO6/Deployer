"""
user object model
"""
from models.base import Base
# tendency of circular import if storage is inported directly
import models
from models.build import Build
from models.user import User
from os import getenv

class DBServer(Base):
    name = "db_server" # collection name
    def __init__(self, user_id, project_id, form=None,  network_id=None):
        self.keys = ["id", "name", "created_at", "user_id", "data_bases",
                     "scope", "db_type", "build_id", "url", "project_id",
                     "user_pass", "user_name"]
        # build id is the combination of build id ans build num
        super().__init__()
        if form:
            self.name = form.dataBaseName.data
            self.db_type = form.dataBaseType.data
            print(self.db_type, "@")
            self.port = form.dataBasePort.data
            self.user_name = form.dataBaseUser.data
            self.user_pass = form.dataBasePass.data
        self.user_id = User.confirm(user_id)
        if project_id:
            self.project_id = project_id #Project.confirm(project_id)
            self.scope = "local"
        else:
            self.scope = "global"
            self.project_id = None
        self.server_ip = getenv("HOST_IP" , "54.208.115.123")
        self.root_pass = "rootpass"
        self.Nid = network_id

    # def create(self):
    def build(self):
        """
        administer a project build
        returns True if it was successfull
        """
        from models.ports import Ports
        if self.project_id:
            network = None
        else:
            network = "create2"
        build = Build(self.id,
                      self.db_type, Nid=self.Nid, projectPort=self.port,
                      userPass=self.user_pass, userName=self.user_name,
                      rootPass=self.root_pass,
                      network=network,
                      relativeProjectId=self.project_id)
        host_port = Ports.get_a_port()
        if not host_port:
            print("No port was gotten, pls log this")
            return False
        self.url = f"{self.server_ip}:{host_port}"
        result = build.build(port=host_port)
        if not result:
            return False
        self.build_id = build.id
        # self.curent build num
        build.save()
        return True

    @classmethod
    def getbuilds(cls, id):
        """
        get the latest build of a project
        """
        results = Build.find({"project_id": id})
        return results
    # def rebuild(self):
    # def addMoreDb(self):
    #     """
    #     manually rebuild a project
    #     """
    #     from models.ports import Ports
    #     project = self.__class__.find({"id": self.id})
    #     if len(project) < 1:
    #         return False
    #     # if no project was found shuld raise error no project found
    #     # re url should be on the project collection istad to a void a new request
    #     # build repo usrol should be unchangable but that of project should be changable in setiogd
    #     project = project[0]
    #     repo_url = Build.find({"id": project["build_id"]}) # to be removed
    #     if len(repo_url) < 1:
    #         return False
    #     repo_url = repo_url[0]["repo"]
    #     build = Build(
    #         self.id,
    #         repo_url,
    #         project["project_type"], project["build_id"])
    #     print("kkkkkkkkkkkkkkkk")
    #     print(project["project_type"])
    #     host_port = Ports.get_a_port()
    #     if host_port == None:
    #         print("No port was gotten, pls log this")
    #         return False
    #     self.url = f"{self.server_ip}:{host_port}"
    #     result = build.rebuild(host_port)
    #     if not result:
    #         return False
    #     self.build_id = build.id
    #     self.built = True
    #     # self.curent build num
    #     self.current_build_num = build.build_num
    #     build.save()
    #     return True

    @classmethod
    def getdatabases(cls, id):
        """
        get the latest build of a project
        """
        results = DBServer.find({"id": id})
        return results

    # @classmethod
    # def getCurentBuild(cls, id, build_num):
    #     result = Build.find({"project_id": id, "build_num": build_num})
    #     if result:
    #         result = result[0]
    #     return result
    # #they currently do the same work this should be fixec
    # @classmethod
    # def getBuildData(cls, id, num):
    #     """
    #     get the output of a build
    #     """
    #     data = None
    #     output = Build.buildOutput(id, num)
    #     status, result = Build.status(id, num)
    #     print("status",status)
    #     data = {"building": status, "result": result, "output":output}
    #     return  data
