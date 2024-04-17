# routes/user.py
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, List, Dict
from ..services.user_queries import (
    create_user,
    get_user_by_username,
    get_current_user,
    authenticate_user,
    get_all_users_service
)
from ..schemas.schema import RegisterUser, LoginUser, CurrentUser
from ..settings.configurations import create_access_token, verify_token, hash_password, verify_password

user_routes = APIRouter(prefix="/api/users")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register User and create its access token
@user_routes.post("/register")
async def register_user(user: RegisterUser):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    user.password = hash_password(user.password)
    db_user = create_user(user)
    access_token = create_access_token(data={"sub": db_user.username})
    response = {"user": db_user, "access_token": access_token, "token_type": "bearer"}
    return {"Success": "User created successfully"}

# Login User and create its access token
@user_routes.post("/login")
async def login_user(user: LoginUser):
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    response = {"user": db_user, "access_token": access_token, "token_type": "bearer"}
    return {"Success": "User logged in successfully"}

@user_routes.get('/get_current_user', response_model=Dict[str, str])
async def get_current_user_details(current_user: CurrentUser = Depends(get_current_user)):
    user_details = {
        "name": current_user.name,
        "username": current_user.username,
        "email": current_user.email,
        "isAdmin": str(current_user.isAdmin)  # Convert bool to str
    }
    return user_details

@user_routes.get('/get_all_users', response_model=List[dict])
async def get_all_users(current_user: CurrentUser = Depends(get_current_user)):
    if not current_user.isAdmin:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
    return get_all_users_service()

