
# The Projenator:  
*I'll be back!*

## Description
This is a CDKv2 project that takes the grind out of setting up new cdk projects/implementations by using automation

When deployed this project will create for each 'template' a set of resources;

- a ssm automation document which 'kicks' off the process of creating a new 'instance' of your template
- a lambda which acts as 'glue' between the ssm automation document and a
- codebuild project which 
	- creates a cdk project based on the parameters you pass into the ssm automation document
	- synths the cdk project
	- deploys the cdk project

## Prerequisites:
- AWS account
- cdkv2 and aws cli tools installed. 

## Assumptions:
- A resonable level of understanding of cdk.

## UseCases:

### python
```
cd python
cdk synth
cdk deploy 
```

Note: the demo template is environment agnostic. If you need to deploy this to a specific account, then use a cdk deploy --profile <yourprofile>

### typescript
<TODO>


## Extending the Templates:
This stack will deploy a set of automation resources for each template that you create.   Use the demo templates as a guide
you need to edit/modify the ssmdocument, potentially the lambda, and also the templates them selves.   The magic is in the .projenrc.js

You also can modify the codebuildproject to change how it deploys the project.  You may want it *NOT* to deploy a cdk project at all, but just create a repo, and place the files in there.
The choice is entirely up to you.   (PR's for example templates welcome)



## References: 

[projen](https://github.com/projen/projen)
[Amazon Cloud Development Kit](https://aws.amazon.com/cdk/)

