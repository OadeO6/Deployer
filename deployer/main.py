#!/usr/bin/env python3
"""
Module that handels the main deployment
"""
import uuid
from os import getenv
import jenkins
from deployer.myxml import generate_xml


class Deployer:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4())) # remove cration od id #temp
        self.server = jenkins.Jenkins(
            url=  getenv("JENKINS_URL","http://localhost:8080"),
            username= getenv("JENKINS_USER", "OadeO6"), # use an env file
            password= getenv("JENKINS_PASSWD", "2a8f52fb4bde48069e2f61049f9b314e")
        )
        self.kwargs = kwargs
        # FLASK_RUN_PORT FLASK_APP
        self.envDict = {}
        self.pType = kwargs.get("projectType", "flask")
        self.repo = kwargs.get("repoUrl") # remove cration od id #temp
        #"https://github.com/Ade06AA/mytest"
        if self.server.job_exists(f"{self.id}-job"):
            self.buildNum = self.server.get_job_info(f'{self.id}-job')['nextBuildNumber']
        else:
            self.buildNum = 1

    def getStatus(self, job_name=None, build_num=None):
        """
        get the status of a build
        returns a tuple that contain:
            building : if the jub is still in building process
            result: the build result
        """
        if job_name is None:
            job_name = f'{self.id}-job'
        if build_num is None:
            build_num = self.buildNum
        status = (None, None)
        try:
            status = self.server.get_build_info(job_name, build_num)
            status = status["building"], status["result"]
        except jenkins.JenkinsException as e:
            pass
        return status

    def getOutput(self, job_name=None, build_num=None):
        """
        get the output of the exicution
        """
        if job_name is None:
            job_name = f'{self.id}-job'
        if build_num is None:
            build_num = self.buildNum
        output = None
        try:
            output = self.server.get_build_console_output(
                job_name, build_num)
        except jenkins.JenkinsException as e:
            pass
        return output

    def getDEnv(self, envDict):
        """
        format the env to be suitable for docker
        """
        env = ""
        for i in envDict:
            emv += " -e {}={} ".format(i, envDict[i])
        return env

    def generate_xml_config(self, host_port):
        code = []
        port = self.envDict.get("FLASK_RUN_PORT", "5000")
        Setup = ["set up ",
                f"sudo docker network  create {self.id}-network",
                "scriptNext", # the script shoud be removed because this file is not meant to understand hoe to interact with jenkins
                 f"""
                 script {{
                    def theRepo = sh(script: "ls -d theRepo-* | head -n 1", returnStdout: true).trim()
                    if (theRepo){{
                            sh "cp -r theRepo theRepo-${{currentBuild.number}}"
                            sh "cd theRepo-${{currentBuild.number}}; git pull"
                        }} else {{
                        sh "git clone {self.repo} theRepo-${{currentBuild.number}}"
                    }}
                }}
                 """]

        pType = self.pType
        if pType:
            if pType.casefold() == "flask":
                Build = ["build flask project"]
                # run container
                Build.append(
                    " sudo docker run -d -it" +
                    f" --name {self.id}-name " +
                    self.getDEnv(self.envDict) +
                    " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
                    " -w /app " +
                    f" -p {host_port}:5000 " +
                    f" --network {self.id}-network" +
                    " python:3.9-alpine " +
                    " sh"
                )
                #do instalations
                Build.append(
                    f"sudo docker exec {self.id}-name sh -c 'pip install -r requirements.txt'"
                )
                Run = ["Run project"]
                # add -d wil make it run in background
                Run.append(
                    f'sudo docker exec -d {self.id}-name sh -c ' +
                    " 'python -m flask --app {} run --host 0.0.0.0' ".format(
                        self.envDict.get("FLASK_APP", "app")
                    )
                )


            if pType.casefold() == "react":
                Build = ["run next project"]
                # run container
                Build.append(
                    "sudo docker run -d -it" +
                    f" --name {self.id}-name " +
                    self.getDEnv(self.envDict) +
                    " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
                    " -w /app " +
                    f" -p {host_port}:3000 " +
                    f" --network {self.id}-network " +
                    " node:16-alpine " +
                    " sh"
                )
                #do instalations
                Build.append(
                    f" sudo docker exec {self.id}-name sh -c 'npm install'"
                )
                Run = ["Run project"]
                Run.append(
                    f"sudo docker exec -d {self.id}-name sh -c 'HOST=0.0.0.0 npm run dev '"
                )

            if pType.casefold() == "next":
                Build = ["run next project"]
                # run container
                Build.append(
                    "sudo docker run -d -it" +
                    f" --name {self.id}-name " +
                    self.getDEnv(self.envDict) +
                    " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
                    " -w /app " +
                    f" -p {host_port}:3000 " +
                    f" --network {self.id}-network " +
                    " node:18-alpine " +
                    " sh"
                )
                #do instalations
                Build.append(
                    f" sudo docker exec {self.id}-name sh -c 'npm install'"
                )
                Run = ["Run project"]
                Run.append(
                    f"sudo docker exec  -d {self.id}-name sh -c 'HOST=0.0.0.0 npm run dev'"
                )
        checkPort = ["skip"]
        code.append(Setup)
        code.append(Build)
        code.append(checkPort)
        code.append(Run)
        print(code)
        xml = generate_xml(self.id, code, port)
        return xml

    def old_data_to_new_repo(self):
        pass

    def get_url(self):
        pass

    def build(self, port, Id=None):
        if not Id:
            try:
                self.server.create_job(
                    f'{self.id}-job', self.generate_xml_config(port)
                )
                self.server.build_job(f"{self.id}-job")
            except Exception as e:
                print("error in creating job")
                raise e
        else:
            b = self.server.build_job(Id+'-job')
            print(b)
            print("*********************** build********************")


    def deploy(self):
        pass

    def destroy(self, Id):
        try:
            self.server.delete_job(f'{self.id}-job')
        except Exception as e:
            print(e)
            print("No such job, BOI")

    def create_agent(self):
        pass
