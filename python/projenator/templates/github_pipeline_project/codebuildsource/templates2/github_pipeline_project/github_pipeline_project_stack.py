from aws_cdk import (
    CustomResource, Stack, Stage,
    pipelines as pipelines,
    aws_codepipeline_actions as codepipeline_actions,
    aws_lambda,
    custom_resources as cr,
    aws_iam as iam
)

import aws_cdk as cdk
from constructs import Construct
from application.application import ExampleApp

class DevStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        ExampleApp(self, "DevExample",
            label='dev'
        )
        
class TestStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        ExampleApp(self, "TestExample",
            label = 'test',
        )

class ProdStage(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        ExampleApp(self, "ProdExample",
            label = 'prod'
        )


class GithubPipelineProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create a github project
        ## custom resource lambda that creates the repo
        create_repo_function = aws_lambda.Function(self, 'CreateGitRepoFunction',
            code= aws_lambda.Code.from_asset(
                path = "./lambda_fn"
            ),
            runtime = aws_lambda.Runtime.PYTHON_3_9,
            handler="creategitrepo.createrepo"
        )
        # give it permission to get to the secret that contains the PAT for github
        create_repo_function.add_to_role_policy(
            statement= iam.PolicyStatement(
                actions = ['secretsmanager:GetSecretValue'],
                resources = ['arn:aws:secretsmanager:<<region>>:<<account>>:secret:<<githubtoken>>'], 
                effect = iam.Effect.ALLOW
            )
        )

        create_repo_provider = cr.Provider(self, "CreateGitRepoProvider",
            on_event_handler=create_repo_function,
        )

        # create a github repo
        GitRepo = CustomResource(self, "CreateGitRepo",
            service_token=create_repo_provider.service_token,
            properties={
                "repo" : "<<repo>>",                                    
                "githubtoken": "<<githubtoken>>"
            }
        )

        #Output the URLS
        cdk.CfnOutput(self, 'GithubRepoCloneURL', 
            description= 'Https Git URL',
            value = GitRepo.get_att_string('clone_url')
        )

        cdk.CfnOutput(self, 'GithubSSHCloneURL', 
            description= 'SSh Git URL',
            value = GitRepo.get_att_string('ssh_url')
        )
        
        cdk.CfnOutput(self, 'GitSecret', 
            description= 'GitSecret',
            value = '<<githubtoken>>'
        )

        cdk.CfnOutput(self, 'FullName', 
            description= 'FullName',
            value = GitRepo.get_att_string('full_name')
        )

        # create a pipeline for the project
        project_pipeline = pipelines.CodePipeline(self, 'Pipeline',
            self_mutation=True,
            synth = pipelines.ShellStep("synth",
                input= pipelines.CodePipelineSource.git_hub(
                    repo = GitRepo.get_att_string('full_repo_name'),                    
                    branch = "<<branch>>",                                              #<<branch>>
                    authentication = cdk.SecretValue.secrets_manager('<<githubtoken>>'),   #<<githubtoken>>
                    trigger = codepipeline_actions.GitHubTrigger.WEBHOOK
                ),
                commands = ["npm ci", "npm run build", "npx cdk synth"]
            )
        )

        # add the Dev stage
        project_pipeline.add_stage(
            DevStage(self, "Dev",
                env = cdk.Environment(
                    account = "<<account>>",                                           #<<account>>
                    region = "<<region>>",                                             #<<region>>
                )
            )
        )
        # add the test stage
        project_pipeline.add_stage(
            TestStage(self, "Test",
                env = cdk.Environment(
                    account = "<<account>>",
                    region = "<<region>>",
                )
            )
        )
        # add the prod stage
        project_pipeline.add_stage(
            ProdStage(self, "Prod",
                env = cdk.Environment(
                    account = "<<account>>",
                    region = "<<region>>",
                )
            )
        )


