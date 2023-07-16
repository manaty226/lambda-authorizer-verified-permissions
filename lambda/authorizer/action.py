class Action:
    actions = {
        "GET": "Read",
        "PUT": "Write"
    }
    action = None
    def __init__(self, http_method):
        self.action = self.actions[http_method]

    def to_avp_action(self):
        return {
            "actionType": "MyBlogApp::Action",
            "actionId": self.action
        }
    