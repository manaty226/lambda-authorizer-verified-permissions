import boto3
from src.action import Action
from src.principal import Principal

class Authorizer:
    client = None
    policy_id = None

    def __init__(self, policy_id):
        self.client = boto3.client('verifiedpermissions')
        self.policy_id = policy_id

    def check_permission(self, token, http_method, blog):
        principal = Principal(token.payload)
        action = Action(http_method)
        resource = blog.to_avp_resource()

        response = None
        try:
            response = self.client.is_authorized_with_token(
                            policyStoreId = self.policy_id,
                            accessToken = token.raw,
                            action = action.to_avp_action(),
                            resource = blog.to_avp_resource(),
                            entities = {
                                "entityList": [
                                    {
                                        "identifier": blog.to_avp_resource(),
                                        "attributes": {
                                            "owner": {
                                                "string": blog.owner
                                            }
                                        }
                                    },
                                    {
                                        "identifier": principal.to_avp_principal(),
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
            return False

        print(response)
        return response is not None and "decision" in response and response["decision"] == "ALLOW"
