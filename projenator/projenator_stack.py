import aws_cdk as cdk

from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_lambda,
    aws_codebuild as codebuild,
    aws_s3_assets as s3_asset,
    aws_iam as iam,
)
from constructs import Construct
import yaml
import os

class ProjenatorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #get the list of templates by walking the templates directory
        templates = [ name for name in os.listdir('projenator/templates') if os.path.isdir(os.path.join('projenator/templates', name)) ]

        
        for template in templates:
            #SSM automation document
            
            with open(f'projenator/templates/{template}/ssm_docs/ssmdocument.yaml', 'r') as ssm_yaml:
                content = yaml.load(ssm_yaml, yaml.Loader)

            ssm.CfnDocument(self, f"{template}-AutomationDocument",
                content = content,
                document_format= 'YAML',
                document_type= 'Automation',
                name= f'Projenator-{template}',
                target_type= '/AWS::Lambda::Function'
            )

            #Lambda function that calls codebuild.
        
            startcodebuild = aws_lambda.Function(self, f"{template}-Function",
                runtime=aws_lambda.Runtime.PYTHON_3_9,
                handler="startprojencodebuild.start",
                code=aws_lambda.Code.from_asset(f'projenator/templates/{template}/lambda_functions'),
                timeout=cdk.Duration.minutes(5),
                function_name = f'{template}-startprojenatorcodebuild'
            )

            #Create an asset for the codebuild source


            asset = s3_asset.Asset(self, f'{template}-codebuildassets',
                path = f"./projenator/templates/{template}/codebuildsource/"
            )

            # Codebuildproject to build and deploy the cdk project 
            cbproject = codebuild.Project(self, "ProjenatorCodebuildProject",
                source=codebuild.Source.s3(
                    bucket=asset.bucket,
                    path = asset.s3_object_key,
                ),
                project_name = f'{template}-projencdkbuilder'
            )

            asset.grant_read(cbproject.role)

            #Give the Lambda permission to start the codebuild
            startcodebuild.add_to_role_policy(
                statement = iam.PolicyStatement(
                    actions = ["codebuild:StartBuild"],
                    resources = [cbproject.project_arn],
                    effect=iam.Effect.ALLOW
                )
            )
