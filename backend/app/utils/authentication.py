from fastapi import Request, status, HTTPException
from .jwt import JWTService
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
algorithm = os.getenv("JWT_ALGORITHM")
secret = os.getenv("JWT_SECRET")

jwt_service = JWTService(secret=secret,algorithm=algorithm)

def get_user_from_token(request:Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt_service.parse_token(auth_header.split(" ")[1]) #removes Bearer
        
        #payload will be dict
        return payload.get('id')
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session has expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
