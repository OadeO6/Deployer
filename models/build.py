"""
user object model
"""
from models.base import Base
import models
from deployer.main import Deployer

class Build(Base):
    name = "build"
    def __init__(self, project_id, _type: str , _repo=None, _id=None,
                 userName=None, userPass=None, rootPass=None, dbName=None,
                 projectPort=None, relativeProjectId=None):
        """
        to add build finis time
        """
        # id is curently useless
        self.keys = ["id", "build_num",
                     "created_at", "project_id",
                    "repo", "building", "status"]
        super().__init__()
        if _id:
            self.id = _id
        self.project_id = project_id
        self.repo = _repo
        _type = _type.lower()
        kwargs = {}
        if _type in ["flask", "react", "next", "django"]:
            kwargs = {"repoUrl": _repo}
        elif _type == "mongodb":
            kwargs = {"userName": userName,"project_id": relativeProjectId,
                     "userPass": userPass}
        elif _type == "mysql":
            kwargs = {"userName": userName, "userPass": userPass,
                     "project_id": relativeProjectId, "rootPass": rootPass}
        self.job = Deployer(id=self.id,
                            projectType=_type, projectPort=projectPort, **kwargs)
        self.build_num = self.job.buildNum

    def build(self, port):
        """
        build
        """
        try:
            self.job.build(port=port)
        except Exception as e:
            models.handleError(e)
            return False
        self.building = True
        self.status = None
        return True

    def rebuild(self, port=None):
        """
        rebuild
        """
        try:
            self.job.build(port, self.id)
        except Exception as e:
            models.handleError(e)
            return False
        self.building = True
        self.status = None
        return True

    @classmethod
    def buildOutput(cls, id, num=None):
        """
        """
        job = Deployer(id=id)
        output = None
        try:
            output = job.getOutput(build_num=num)
        except Exception as e:
            raise e
        return output

    @classmethod
    def status(cls, id, num=None):
        """
        """
        job = Deployer(id=id)
        status = (None, None)
        try:
            print("status")
            status = job.getStatus(build_num=num)
            print(status)
        except Exception as e:
            raise e
        return status

    @classmethod
    def updateBuildStat(cls, obj, caller=None):
        """
        update database
        """
        stats= cls.status(obj["id"], obj["build_num"])
        models.storage.update(cls, obj,
                              {
                              "building": False if caller == "jenkins" else stats[0],
                              "status": stats[1]
                              })
