from pydantic import BaseModel


class AuthorizationSchema(BaseModel):
    access_token: bytes
    refresh_token: bytes
    expires_in: int = 15*60
