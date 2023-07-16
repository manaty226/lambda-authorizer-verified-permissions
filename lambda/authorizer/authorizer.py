import boto3
from action import Action
from principal import Principal

class Authorizer:
    client = None
    policy_id = None
    blog_repository = None

    def __init__(self, policy_id, blog_repository):
        self.client = boto3.client('verifiedpermissions')
        self.policy_id = policy_id
        self.blog_repository = blog_repository

    def check_permission(self, token, http_method, resource_id):
        principal = Principal(token.payload)
        action = Action(http_method)
        blog = self.blog_repository.find_by_id(resource_id, principal.subject())
        resource = blog.to_json_resource()

        response = None
        try:
            response = self.client.is_authorized_with_token(
                policyStoreId = self.policy_id,
                accessToken = token.raw,
                action = action.to_avp_action(),
                resource = resource,
                entities = {
                    "entityList": [
                        {
                            "identifier": resource,
                            "attributes": {
                                "owner": blog.owner
                            }
                        },
                        {
                            "identifier": principal.to_principal_json(),
                            "attributes": {
                                "sub": {
                                    "string": principal.subject()
                                }
                            }

                        }
                    ]
                }
            )
        except Exception as e:
            print(e)
            print(response)

        return "decision" in response and response["decision"] == "ALLOW"
