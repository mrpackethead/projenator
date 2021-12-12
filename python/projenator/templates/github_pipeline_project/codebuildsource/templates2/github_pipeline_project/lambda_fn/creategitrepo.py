import urllib3
import json
import requests
import boto3
from requests.structures import CaseInsensitiveDict

SUCCESS = 'SUCCESS'
FAILED = 'FAILED'

http = urllib3.PoolManager()

def cfn_response_send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)


    except Exception as e:
        print("send(..) failed executing http.request(..):", e)



def createrepo(event, context):

	if event['RequestType'] == 'Create':

		sm = boto3.client('secretsmanager')

		githubtoken = sm.get_secrect_value(
			SecretId = event['ResourceProperties']['githubtoken']
		)['SecretString']['Token']
		
		# curl -H "Authorization: token ACCESS_TOKEN" --data '{"name":"NEW_REPO_NAME"}' https://api.github.com/user/repos

		url = "https://api.github.com/user/repos"
		headers = CaseInsensitiveDict()
		headers["Authorization"] = f"token {githubtoken}"
		headers["Content-Type"] = "application/x-www-form-urlencoded"
		data = {"name": f"{event['ResourceProperties']['githubtoken']}"}

		request = requests.post(url, headers=headers, data=data)


		if request.status_code == '201':
			cfn_response_send(event, context, SUCCESS,    
				reason = f"Repo {event['ResourceProperties']['repo']} created. See the details in CloudWatch Log Stream {context.log_stream_name}",
				responseData= 
				{
					"clone_url": f"{request.text['clone_url']}",
  					"ssh_url": f"{request.text['ssh_url']}",
					"full_repo_name": f"{request.text['full_name']}"
				}
			)
		else:
			cfn_response_send(event,context, FAILED, 
				reason = f"Repo {event['ResourceProperties']['repo']} creation Failed. See the details in CloudWatch Log Stream {context.log_stream_name}",
				responseData={}
			)


	elif event['RequestType'] in ['Update', 'Delete']:
		cfn_response_send(event, context, SUCCESS,
			reason = f"Repo {event['ResourceProperties']['repo']} is immutable, no changes occured. See the details in CloudWatch Log Stream {context.log_stream_name}",
			responseData= {}
		)

	else:
		cfn_response_send(event, context, FAILED,
			reason = f"Invalid Request Type See the details in CloudWatch Log Stream {context.log_stream_name}",
			responseData= {}
		)
