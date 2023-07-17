from urllib.parse import urlparse

class Principal:
    claims = {}
    def __init__(self, payload):
        self.claims = payload
    
    def to_avp_principal(self):
        user_pool_id = urlparse(self.claims["iss"]).path.split("/")[1]
        return {
            "entityType": "MyBlogApp::User",
            "entityId": user_pool_id + "|" + self.claims["sub"]
        }
    
    def subject(self):
        return self.claims["sub"]