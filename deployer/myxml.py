def generate_pipe(Id, code, port, apiEndpoint, check, abort, fail):
    """
    create a pieline code using the two di,entional list of commands
    """
    stages = ""
    for i in code:
        if i[0] == "skip":
            stages += (f'\n\t\t\tstage("Checkin port"){{\n\t\t\t\tsteps {{' +
            '\n\t\t\t\t\tscript {'+
            f'\n\t\t\t\t\t\tdef status = sh(script: \'sudo docker exec  {Id}-name -c \"netstat -tnlp | grep {port}\"\', returnStatus: true)\n\t\t\t\t\t\tif (status == 0) {{\n\t\t\t\t\t\t\tcurrentBuild.result = \'FAILURE\'\n\t\t\t\t\t\t\techo \'commande failed costum\'\n\t\t\t\t\t\t}} else {{\n\t\t\t\t\t\t\tcurrentBuild.result = \'SUCCESS\'\n\t\t\t\t\t\t}}' +
            '\n\t\t\t\t\t}\n' +
            '\n\t\t\t\t}\n\t\t\t}\n'
        )
            continue
        stage = f'\n\t\t\tstage("{i[0]}"){{\n\t\t\t\tsteps {{'
        for j in i[1:]:
            if j == "scriptNext":
                # it is expected that there is only one script stage left
                stage += '\n\t\t\t\t\t{}'.format(i[-1])
                break
            step = '\n\t\t\t\t\tsh "{}"'.format(j)
            stage += step
        stage += "\n\t\t\t\t}\n\t\t\t}\n"
        stages += stage
        # agent {{ label 'alx' }}
    # had to do it this way because in python f string regects any backlash
    # something like a = f" { 'ade\n' }" wount work
    # commenting is also not allowed
    stagesContent = (
                '\tstage("healt check"){\n' +
                    "\t\toptions {\n" +
                        "\t\t\tretry(40)\n" +
                   "\t\t}\n" +
                    "\t\tsteps {\n" +
                        '\t\t\techo "cheacking if server is ready"\n' +
                        f"\t\t\tsh \"sudo docker exec { Id }-name sh -c 'netstat -tnlp | grep { port }'\"\n" +
                        f"\t\t\techo 'Server listenig on { port } '\n" +
                    "\t\t}\n" +
                "\t}\n" if check else "")
    abort = [a+'\n' for a in abort]
    fail = [a+'\n' for a in fail]
    pipeline_code = f"""pipeline {{
        agent {{ label 'alx'}}

        triggers {{
            pollSCM('*/1 * * * *')
        }}
        stages {{
        { stages }
            {
                stagesContent
            }
        }}
        post {{
            aborted {{
                {
                "".join(abort)
                }
            }}
            failure {{
                {
                    "".join(fail)
                }
            }}
            always {{
                echo 'done with { Id }'
                script {{
                    def original = currentBuild.currentResult
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){{
                         def response = httpRequest(httpMode: 'PUT', url: '{ apiEndpoint }', contentType: 'APPLICATION_JSON')
                         echo "Status: ${{response.status}}"
                    }}
                    currentBuild.result = original
                }}
            }}
        }}
    }}"""
    return pipeline_code

def generate_xml(Id, code=[[]], port=None,
                 apiEndpoint=None, check=False,
                 abort=["echo 'no command to run after abort'"],
                 fail=["echo 'no command to run after fail'"],
                 description="no description"):
    pipeline_code = generate_pipe(Id, code, port, apiEndpoint, check, abort, fail)
    xml_config = f"""<?xml version="1.1" encoding="UTF-8" standalone="no"?>
    <flow-definition plugin="workflow-job@1400.v7fd111b_ec82f">
      <actions>
        <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@2.2198.v41dd8ef6dd56"/>
        <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@2.2198.v41dd8ef6dd56">
          <jobProperties/>
          <triggers/>
          <parameters/>
          <options/>
        </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
      </actions>
      <description>{ description }</description>
      <keepDependencies>false</keepDependencies>
      <properties>
      </properties>
      <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@3894.3896.vca_2c931e7935">
        <script>{ pipeline_code }</script>
        <sandbox>true</sandbox>
      </definition>
      <triggers/>
      <disabled>false</disabled>
    </flow-definition>"""
    return xml_config
