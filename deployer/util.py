def nodeSetup(code, Id, Nid, dockerEnv, mainEnv, host_port, Type, kwargs):
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
        f" --network { Nid }-network " +
        " node:21.7.1-alpine " +
        " sh"
    )
    #do instalations
    Build.append("echo '+ @show2@ Installing Dependencies...'")
    installCommand = kwargs.get('installCommand')
    if not installCommand:
        installCommand = 'npm install'
        # do some filtering first
    Build.append(
        f"sudo docker exec {Id}-name sh -c '{installCommand}'"
    )
    Run = ["Run project"]
    runCommand = kwargs.get('runCommand')
    if not runCommand:
        runCommand = "HOST=0.0.0.0 npm run dev"
        # do some filtering first
    Run.append(
        f"sudo docker exec -d {Id}-name sh -c '{runCommand}' #show1# run project "
    )
    # Run.append(
    #     f"sudo docker exec -d { Id }-name sh -c 'HOST=0.0.0.0 npm run dev '"
    # )
    checkPort = ["skip"]
    code.append(Build)
    code.append(checkPort)
    code.append(Run)
    return code, projectPort

def pythonSetup(code, Id, Nid, dockerEnv, mainEnv, host_port, Type,  kwargs):
    if Type == "django":
        projectPort = 8000
    elif Type == "flask":
        projectPort = 5000
    else:
        projectPort = 5000
    Build = ["build flask project"]
    # run container
    Build.append(
        " sudo docker run -d -it" +
        f" --name {Id}-name " +
        dockerEnv +
        " -v \$(pwd)/theRepo-${currentBuild.number}:/app " +
        f" -w /app/{kwargs.get('projectDir')} " +
        f" -p {host_port}:{projectPort} " +
        f" --network {Nid}-network" +
        " python:3.9-alpine " +
        " sh"
    )
    #do instalations
    Build.append("echo '+ @show1@ Installing Dependencies...'")
    Build.append("echo '+ @show2@ Installing Dependencies...'")
    installCommand = kwargs.get('installCommand')
    if not installCommand:
        installCommand = 'pip install -r requirements.txt'
        # do some filtering first
    Build.append(
        f"sudo docker exec {Id}-name sh -c '{installCommand}'"
    )
    Run = ["Run project"]
    # add -d wil make it run in background
    # Run.append(
    #     f'sudo docker exec -d {Id}-name sh -c ' +
    #     " 'python -m flask --app {} run --host 0.0.0.0' ".format(
    #         mainEnv.get("FLASK_APP", "app")
    #     )
    # )
    runCommand = kwargs.get('runCommand')
    if Type ==  "django":
        runCommand = f" python manage.py runserver {projectPort}"
    elif Type ==  "python":
        runCommand = " python -m flask --app {} run --host 0.0.0.0 --port {} ".format(
            mainEnv.get("FLASK_APP", "app"), projectPort
        )
    elif Type == "flask":
        runCommand = " python -m flask --app {} run --host 0.0.0.0 --port {} ".format(
            mainEnv.get("FLASK_APP", "app"), projectPort
        )
    else:
        runCommand = " python -m flask --app {} run --host 0.0.0.0 --port {} ".format(
            mainEnv.get("FLASK_APP", "app"), projectPort
        )
    # do some filtering first
    Run.append(
        f"sudo docker exec -d {Id}-name sh -c '{runCommand}' #show1# run project "
    )
    checkPort = ["skip"]
    code.append(Build)
    code.append(checkPort)
    code.append(Run)
    return code, projectPort

def mysqlSetup(code, Id, Nid, dockerEnv, mainEnv, host_port,
               dbDetails, parentId=None, dbName=None):
    """
    create a mysql database
    """
    userName = dbDetails.get("userName")
    userPass = dbDetails.get("userPass")
    rootPass = dbDetails.get("rootPass")
    dbPort = dbDetails.get("projectPort")
    print(dbPort)
    if not dbPort:
        dbPort = 3306
    print(dbPort)
    parentId = dbDetails.get("parent_id")
    if parentId:
        parentId = parentId
        portMapping = f" -p {host_port}:{dbPort} "
    else:
        parentId = Id
        portMapping = f" -p {host_port}:{dbPort} "
    CreateServer = ["create data-base server"]
    CreateServer.append(
        f" sudo docker run --name {Id}-name " +
        portMapping +
        f" --network {Nid}-network" +
        f"  -e MYSQL_ROOT_PASSWORD={rootPass} " +
        f" -e MYSQL_USER={userName} " +
        f" -e MYSQL_TCP_PORT={dbPort} " +
        f" -e MYSQL_PASSWORD={userPass} " +
        " -d mysql:8.0 "
    )
    CreateDatabase = ["create data-base"]
    CreateDatabase.append(
        f" sudo  docker run -it --rm  mysql:8.0  " +
        # f" mysql -u{userName} -p{userPass} -P {projectPort}" +
        f" mysql -uroot -p{rootPass} -P {dbPort}" +
        f" -e CREATE DATABASE {dbName}; "
    )
    CreateDatabase.append(
        f" sudo  docker run -it --rm  mysql:8.0  " +
        # f" mysql -u{userName} -p{userPass} -P {projectPort}" +
        f" mysql -uroot -p{rootPass} -P {dbPort}" +
    f" GRANT ALL PRIVILEGES ON {dbName}.* TO '{userName}'@'%'; "
    )
    code.append(CreateServer)
    #code.append(CreateDatabase)
    return code, dbPort

def mongodbSetup(code, Id, Nid,  dockerEnv, mainEnv, host_port, dbDetails):
    """
    create a mysql database
    """
    userName = dbDetails.get("userName")
    userPass = dbDetails.get("userPass")
    parentId = dbDetails.get("parent_id")
    dbPort = dbDetails.get("projectPort")
    print(dbDetails, "yes")
    if not dbPort:
        dbPort = 27017
    if parentId:
        parentId = parentId
        portMapping = f" -p {host_port}:{dbPort} "
    else:
        parentId = Id
        portMapping = f" -p {host_port}:{dbPort} "
    CreateServer = ["create data-base server"]
    CreateServer.append(
        f" sudo docker run --name {Id}-name " +
        portMapping +
        f" --network {Nid}-network" +
            f" -e MONGO_INITDB_ROOT_USERNAME={userName} " +
            f" -e MONGO_PORT={dbPort} " +
            f" -e MONGO_INITDB_ROOT_PASSWORD={userPass} " +
            " -d mongo:3.6.13-xenial "
            # " -d mongo:7.0-jammy "
    )
    code.append(CreateServer)
    return code, dbPort

    # there should be no need to create a dfata base since it will
    # be automatically created
    # CreateDatabase = ["create data-base"]
    # CreateDatabase.append(
    #     f" sudo  docker exec -it {Id}-name-${{currentBuild.number}} mongosh " +
    #     f" -u {userName} -p {userPass} -P {projectPort}" +
    #     f" CREATE DATABASE {dbName} "
    # )
    # code.append(CreateServer)
    # code.append(CreateDatabase)
