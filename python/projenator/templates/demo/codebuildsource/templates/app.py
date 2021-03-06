import aws_cdk as cdk
from aws_cdk import (
    Stack,
)
from constructs import Construct

class Default(Stack):

	def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
		super().__init__(scope, construct_id, **kwargs)

		cdk.CfnOutput(self, 'DefaultOutput', 
			value = 'default'
		)

app = cdk.App()
Default(app, '<<name>>')
app.synth()

