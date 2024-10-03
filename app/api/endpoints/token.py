from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.jwt_utils import create_access_token
from app.utils.token_storage import TokenStorage
from app.core.config import settings
from datetime import datetime, timedelta

router = APIRouter()
USERNAME = settings.USER_NAME
PASSWORD = settings.PASS_WORD


@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != USERNAME or form_data.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username + form_data.password + str(datetime.now())}, expires_delta=access_token_expires
    )
    TokenStorage.set_token(access_token)
    return {"access_token": access_token, "token_type": "bearer"}
