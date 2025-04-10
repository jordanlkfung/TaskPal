import jwt

class JWTService():
    def __init__(self, secret:str, algorithm:str):
        self._secret = secret
        self._algorithm = algorithm
        
    def create_token(self, payload:dict) -> str:
        return jwt.encode(
            payload,
            self._secret,
            algorithm = self._algorithm,
            headers={"exp": 60 * 60 * 24 * 7} #7 days
        )
    
    def parse_token(self, token:str) -> dict:
        return jwt.decode(token, key=self._secret, algorithms=[self._algorithm])

