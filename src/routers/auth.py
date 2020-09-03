from controllers.auth import AuthorizationController
from schemas.auth import AuthorizationSchema
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Body, Depends
from routers import CustomRouter

router = CustomRouter()


@router.post("/token", response_model=AuthorizationSchema)
async def authenticate(user_data: OAuth2PasswordRequestForm = Depends()):
    return AuthorizationController.authenticate(user_data.username, user_data.password)


@router.post("/refresh", response_model=AuthorizationSchema)
async def refresh_token(token: str = Body(..., embed=True, alias="refresh_token")):
    return AuthorizationController.refresh_token(token)
