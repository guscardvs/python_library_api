from routers import (
    CustomRouter,
    users,
    auth
)
from controllers.auth import AuthorizationController
from fastapi import Depends

router = CustomRouter()

router.include_router(users.router, prefix="/users",
                      tags=["Usuários"], dependencies=[Depends(AuthorizationController.scan_token)])

router.include_router(auth.router, tags=["Autenticação"])
