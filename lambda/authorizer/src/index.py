import boto3
import os
from src.authorizer import Authorizer
from src.token import Token
from src.blog_repository import BlogRepository

def lambda_handler(event, context):
  
  print('boto3 vertion is {0}'.format(boto3.__version__))
  print(event)  
  
  token = Token.parse(event["headers"]["Authorization"].split(" ")[1]) 
  http_method = event["httpMethod"]
  resource_id = event["path"].split("/")[-1]

  blog_repository = BlogRepository()
  blog = blog_repository.find_by_id(resource_id, token.payload["sub"])
  
  isAuthorized = False
  if blog is not None:
    authorizer = Authorizer(policy_id=os.environ["POLICY_ID"])
    isAuthorized = authorizer.check_permission(token, http_method, blog)

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
