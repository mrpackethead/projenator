import json
import boto3

def start(event, context):
    envars = []
    for key,value in event['env_var'].items():
        envars.append(
            {
                'name': key,
                'value': value,
                'type': 'PLAINTEXT'
            }

	# At this point it is highly recommended that you may want to sanity check the enviroment
	# variables you get.  For example, you may want to check to see if this stack already exisits 
	# to prevent overwriting it. This is left to the reader.


    codebuild = boto3.client('codebuild')
    response = codebuild.start_build(
        projectName = 'projencdkbuilder',
        environmentVariablesOverride = envars,
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Started The codebuild process that will process the templates, with projen and deploy them with cdk')
    }
