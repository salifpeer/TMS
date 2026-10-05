from datetime import datetime, timedelta, timezone
<<<<<<< HEAD

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError


SECRET_KEY = "abd"
ALGORITHM = "HS256"

security = HTTPBearer()


=======
 
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
 
 
SECRET_KEY = "abd"
ALGORITHM = "HS256"
 
security = HTTPBearer()
 
 
>>>>>>> 16b938c4ceecd7ac45a86ff7160d043ff2cff9d1
def create_token(email):
 
    expire = (
        datetime.now(timezone.utc)
        + timedelta(hours=1)
    )
 
    data = {
        "sub": email,
        "exp": expire
    }
 
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
<<<<<<< HEAD

    return token


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

=======
 
    return token
 
 
def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
 
    token = credentials.credentials
 
    try:
 
>>>>>>> 16b938c4ceecd7ac45a86ff7160d043ff2cff9d1
        jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
<<<<<<< HEAD

        return True

    except JWTError:

=======
 
        return True
 
    except JWTError:
 
>>>>>>> 16b938c4ceecd7ac45a86ff7160d043ff2cff9d1
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )