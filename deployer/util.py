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
    if True:
        parentId = Id
    CreateServer = ["create data-base server"]
    CreateServer.append(
        f" sudo docker run --name {Id}-name " +
        f" -p {host_port}:{projectPort} " +
        f" --network {parentId}-network-${{currentBuild.number}}" +
        f"  -e MYSQL_ROOT_PASSWORD={rootPass} " +
        f" -e MYSQL_USER={userName} " +
        f" -e MYSQL_TCP_PORT={projectPort} " +
        f" -e MYSQL_PASSWORD={userPass} " +
        " -d mysql:8.0 "
    )
    CreateDatabase = ["create data-base"]
    CreateDatabase.append(
        f" sudo  docker run -it --rm  mysql:8.0  " +
        # f" mysql -u{userName} -p{userPass} -P {projectPort}" +
        f" mysql -uroot -p{rootPass} -P {projectPort}" +
        f" -e CREATE DATABASE {dbName}; "
    )
    CreateDatabase.append(
        f" sudo  docker run -it --rm  mysql:8.0  " +
        # f" mysql -u{userName} -p{userPass} -P {projectPort}" +
        f" mysql -uroot -p{rootPass} -P {projectPort}" +
    f" GRANT ALL PRIVILEGES ON {dbName}.* TO '{userName}'@'%'; "
    )
    code.append(CreateServer)
    code.append(CreateDatabase)
    return code

def mongodbSetup(code, Id, dockerEnv, mainEnv, host_port):
    """
    create a mysql database
    """
    CreateServer = ["create data-base server"]
    CreateServer.append(
        f" sudo docker run --name {Id}-name " +
        f" --network {parentId}-network-${{currentBuild.number}}" +
            f" -e MONGO_INITDB_ROOT_USERNAME={userName} " +
            # f" -e MYSQL_TCP_PORT={projectPort} " +
            f" -e MONGO_INITDB_ROOT_PASSWORD={userPass} " +
            " -d mongo:7.0-jammy "
    )

    # there should be no need to create a dfata base since it will
    # be automatically created
    # CreateDatabase = ["create data-base"]
    # CreateDatabase.append(
    #     f" sudo  docker exec -it {Id}-name mongosh " +
    #     f" -u {userName} -p {userPass} -P {projectPort}" +
    #     f" CREATE DATABASE {dbName} "
    # )
    # code.append(CreateServer)
    # code.append(CreateDatabase)
