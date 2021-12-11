import aws_cdk as cdk
from projenator.projenator_stack import ProjenatorStack

app = cdk.App()
ProjenatorStack(app, "ProjenatorStack")
app.synth()
