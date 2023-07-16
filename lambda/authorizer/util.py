class Action:
    @staticmethod
    def http_method_to_action(self, http_method):
        return {
            "actionType": "Action",
            "actionId": self.__action_id(http_method)
        }
    
    def __action_id(self, http_method):
        return "Read" if http_method == "GET" else "Write"