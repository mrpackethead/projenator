import aws_cdk as cdk
from aws_cdk import (
    Stack,
)
from constructs import Construct

class Default(Stack):

	def __init__(self, scope: Construct, construct_id: str, parameters, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		cdk.CfnOutput(self, 'DefaultOutput', 
			value = parameters['env_parameters']['name']
		)
