import aws_cdk as cdk
from aws_cdk import (
    Stack,
)
from constructs import Construct

class ExampleApp(Stack):

	def __init__(self, scope: Construct, construct_id: str, label: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		cdk.CfnOutput(self, label, 
			value = label
		)