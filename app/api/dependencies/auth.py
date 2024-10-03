from fastapi import HTTPException, status
from app.utils.token_storage import TokenStorage
from app.utils.jwt_utils import decode_access_token


async def get_current_user():
    try:
        token = TokenStorage.get_token()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = decode_access_token(token)
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
