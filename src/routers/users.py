from routers import CustomRouter, get_filters
from schemas.users import (
    UserResponseSchema,
    RegisterSchema
)
from fastapi import (
    Query,
    Body,
    Path,
    Depends
)
from controllers.users import UserController
from controllers.auth import AuthorizationController
from typing import Iterable
from datetime import date
from pydantic import EmailStr

router = CustomRouter()


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user(id: str = Path(...)):
    user_controler = UserController()
    return user_controler.get(id)


@router.get("/", response_model=Iterable[UserResponseSchema])
async def list_users(username: str = Query(None), email: EmailStr = Query(None), birth_date: date = Query(None), active: bool = Query(None), user=Depends(AuthorizationController.scan_token)):
    filters = get_filters(locals(), ["user"])
    user_controler = UserController(user)
    return user_controler.fetch(filters)


@router.post("/", response_model=UserResponseSchema)
async def create_user(user_data: RegisterSchema):
    user_controler = UserController()
    return user_controler.create(user_data.dict())


@router.put("/{id}", response_model=UserResponseSchema)
async def edit_user(id: str, user_data: RegisterSchema.EditSchema):
    user_controler = UserController()
    return user_controler.update(id, user_data.dict())


@router.delete("/{id}")
async def delete_user(id: str):
    user_controler = UserController()
    user_controler.delete(id)
