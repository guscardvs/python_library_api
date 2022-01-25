from controllers.users import UserController
from controllers import BaseController
import jwt
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import (
    HTTPException,
    Depends,
    Request
)
from typing import Tuple
from settings import PROJECT_KEY
from datetime import timedelta, datetime
from schemas.auth import AuthorizationSchema
from functools import wraps


class CustomOAuth2PWDBearer(OAuth2PasswordBearer):

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() not in ["bearer", "jwt"]:
            raise HTTPException(401, detail="Not authenticated", headers={
                                "WWW-Authenticate": "Bearer"})
        return param


oauth_scheme = CustomOAuth2PWDBearer(tokenUrl="/token")


class AuthorizationController:

    def get_user_by_username(self, username):
        user_controller = UserController()
        user = user_controller.fetch({'username': username}, raw=True)
        if not user:
            raise HTTPException(404, detail="Invalid credentials")
        return user[0]

    def verify_user(self, user: UserController.model, password: str):
        if not user.verify_password(password):
            raise HTTPException(401, detail="Invalid credentials")

    def get_user(self, *, id: str = None, credentials: Tuple[str, str] = None) -> UserController.model:
        if id:
            return UserController().get(id, raw=True)
        if not credentials:
            raise HTTPException(404, detail="User not found")
        username, password = credentials
        user = self.get_user_by_username(username)
        self.verify_user(user, password)
        return user

    @classmethod
    def refresh_token(cls, token: str):
        try:
            user_id = jwt.decode(token, PROJECT_KEY, algorithms=[
                                 "HS512"]).get("sub")
            assert user_id and "$refresh" in user_id
        except jwt.PyJWTError:
            raise HTTPException(401, detail="Invalid or expired token")
        except AssertionError:
            raise HTTPException(401, detail="Invalid or expired token")
        auth = cls()
        user = auth.get_user(id=user_id.replace("$refresh", ""))
        auth.create_token(user)
        return AuthorizationSchema(access_token=auth.token, refresh_token=auth.refresh_token)

    @classmethod
    def scan_token(cls, token: str = Depends(oauth_scheme)):
        try:
            user_id = jwt.decode(token, PROJECT_KEY,
                                 algorithms=["HS512"]).get("sub")
            assert user_id and "$refresh" not in user_id
        except jwt.PyJWTError:
            raise HTTPException(401, detail="Invalid or expired token")
        except AssertionError:
            raise HTTPException(401, detail="Invalid or expired token")
        auth = cls()
        return auth.get_user(id=user_id)

    def create_token(self, user):
        expiration = datetime.utcnow() + timedelta(minutes=15)
        refresh_expiration = datetime.utcnow() + timedelta(days=60)
        data = {
            "sub": "%s" % user.pk,
            "exp": expiration
        }
        refresh = {
            "sub": "%s$refresh" % user.pk,
            "exp": refresh_expiration
        }
        self.token = jwt.encode(data, PROJECT_KEY, algorithm="HS512")
        self.refresh_token = jwt.encode(
            refresh, PROJECT_KEY, algorithm="HS512")

    @classmethod
    def authenticate(cls, username, password):
        auth = cls()
        if not username or not password:
            raise HTTPException(400, detail="Username or password missing")
        user = auth.get_user(credentials=(username, password))
        auth.create_token(user)
        return AuthorizationSchema(access_token=auth.token, refresh_token=auth.refresh_token)
