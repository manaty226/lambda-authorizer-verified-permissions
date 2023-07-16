import boto3
import os
from authorizer import Authorizer
from token import Token
from blog_repository import BlogRepository

def lambda_handler(event, context):

  token = Token.parse(event["headers"]["authorization"].split(" ")[1]) 
  http_method = event["httpMethod"]
  resource_id = event["path"].split("/")[-1]

  blog_repository = BlogRepository()
  authorizer = Authorizer(policy_id=os.environ["POLICY_ID"], blog_repository=blog_repository)
  isAuthorized = authorizer.check_permission(token, http_method, resource_id)

  effect = "Deny"
  if isAuthorized:
    effect = "Allow"

  return {
      'principalId': '*',
      'policyDocument': {
          'Version': '2012-10-17',
          'Statement': [
              {
                  'Action': 'execute-api:Invoke',
                  'Effect': effect,
                  'Resource': event['methodArn']
              }
          ]
      }
  }
