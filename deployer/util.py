def reactSetup(code, Id, dockerEnv, mainEnv, host_port):
    projectPort = 3000 # or get costum port
    Build = ["run next project"]
    # run container
    Build.append(
        "sudo docker run -d -it" +
        f" --name {Id}-name " +
        dockerEnv  +
        " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
        " -w /app " +
        f" -p {host_port}:{projectPort  } " +
        f" --network { Id }-network-${{currentBuild.number}} " +
        " node:16-alpine " +
        " sh"
    )
    #do instalations
    Build.append(
        f" sudo docker exec { Id }-name sh -c 'npm install'"
    )
    Run = ["Run project"]
    Run.append(
        f"sudo docker exec -d { Id }-name sh -c 'HOST=0.0.0.0 npm run dev '"
    )
    checkPort = ["skip"]
    code.append(Build)
    code.append(checkPort)
    code.append(Run)
    return code, projectPort

def flaskSetup(code, Id, dockerEnv, mainEnv, host_port):
    projectPort = 5000
    Build = ["build flask project"]
    # run container
    Build.append(
        " sudo docker run -d -it" +
        f" --name {Id}-name " +
        dockerEnv +
        " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
        " -w /app " +
        f" -p {host_port}:{projectPort} " +
        f" --network {Id}-network-${{currentBuild.number}}" +
        " python:3.9-alpine " +
        " sh"
    )
    #do instalations
    Build.append(
        f"sudo docker exec {Id}-name sh -c 'pip install -r requirements.txt'"
    )
    Run = ["Run project"]
    # add -d wil make it run in background
    Run.append(
        f'sudo docker exec -d {Id}-name sh -c ' +
        " 'python -m flask --app {} run --host 0.0.0.0' ".format(
            mainEnv.get("FLASK_APP", "app")
        )
    )
    checkPort = ["skip"]
    code.append(Build)
    code.append(checkPort)
    code.append(Run)
    return code

def mysqlSetup(code, Id, dockerEnv, mainEnv, host_port):
    """
    create a mysql database
    """
    CreateServer = ["create data-base server"]
    CreateDatabase = ["create data-base"]
    code.append(CreateServer)
    code.append(CreateDatabase)
    return code
