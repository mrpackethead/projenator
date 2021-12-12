#!/usr/bin/env python3
import os

import aws_cdk as cdk

from github_pipeline_project.github_pipeline_project_stack import GithubPipelineProjectStack


app = cdk.App()
GithubPipelineProjectStack(app, "<<projectname>>",
    env = cdk.Environment(
        account = '<<account>>',
        region = '<<region>>'
    )
)

app.synth()
