class Principal:
    claims = {}
    def __init__(self, payload):
        self.claims = payload
    
    def to_avp_principal(self):
        return {
            "entityType": "MyBlogApp::User",
            "entityId": self.claims["iss"] + "|" + self.claims["sub"]
        }
    
    def subject(self):
        return self.claims["sub"]
    