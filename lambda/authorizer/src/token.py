import json
import base64

class Token:
    raw = None
    header = None
    payload = None
    signature = None
    
    def __init__(self, raw:str, header:str, payload:str, signature:str) -> None:
        self.header = header
        self.payload = payload
        self.signature = signature
        self.raw = raw
    
    @staticmethod
    def parse(bearer_token:str):
        jwt = bearer_token.split(".")
        header = json.loads(Token.__base64_decode(jwt[0]))
        payload = json.loads(Token.__base64_decode(jwt[1]))
        signature = jwt[2]   
        return Token(bearer_token, header, payload, signature)

    def sub(self)->str:
        return self.payload["sub"]

    @staticmethod
    def __base64_decode(data):
        return base64.b64decode(data + "=" * (-len(data) % 4)).decode()