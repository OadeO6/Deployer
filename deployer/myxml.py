sample_pipeline_code = """pipeline {
    agent any
    stages {
        stage("discription"){
            steps {
                sh "echo run"
            }
        }
    }
}"""

def generate_pipe(Id, code, port):
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
    pipeline_code = """pipeline {{
        agent any

        triggers {{
            pollSCM('*/1 * * * *')
        }}
        stages {{
        {}
            stage("healt check"){{
                options {{
                    retry(40)
                }}
                steps {{
                    echo "cheacking if server is ready"
                    sh "sudo docker exec {}-name sh -c 'netstat -tnlp | grep {}'"
                    echo 'Server listenig on {} '
                }}
            }}
        }}
        post {{
            aborted {{
                sh "sudo docker rm -f {}-name"
                sh "sudo docker network rm {}-network"
            }}
            failure {{
                sh "sudo docker rm {}-name -f"
                sh "sudo docker network rm {}-network"
            }}
            always {{
                echo 'done with {}'
            }}
        }}
    }}""".format(stages, Id, port, port, Id, Id, Id, Id, Id)
    return pipeline_code

def generate_xml(Id, code=None, port=None, description="no description"):
    if not code:
        code = [[]]
    pipeline_code = generate_pipe(Id, code, port)
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
