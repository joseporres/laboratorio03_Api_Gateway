import json

#authorization

def lambda_handler(event, context):
    if event['headers']['Authorization'] == '1234':
        principalId = 'user'
        policyDocument = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": event['methodArn']
                }
            ]
        }
    else:
        principalId = 'unauthorized'
        policyDocument = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Deny",
                    "Resource": event['methodArn']
                }
            ]
        }
    return {
        "principalId": principalId,
        "policyDocument": policyDocument
    }
    
