from ..db.db_setup import db
from ..models.models import User as UserDB
from ..schemas.schema import User as UserSchema
from ..settings.configurations import verify_password

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..settings.configurations import verify_token
from ..schemas.schema import CurrentUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create User
def create_user(user: UserSchema):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get User By ID
def get_user(user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()

# Get User By Email
def get_user_by_email(email: str):
    return db.query(UserDB).filter(UserDB.email == email).first()

# authenticate user
def authenticate_user(username: str, password: str):
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user

# Get User by Username
def get_user_by_username(username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()

# Get Current User
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Fetch user details from the database based on the username
        user = get_user_by_username(username)
        if user is None:
            raise credentials_exception
    except:
        raise credentials_exception
    # Return CurrentUser object with user details
    return CurrentUser(name=user.name, username=user.username, email=user.email, isAdmin=user.isAdmin)

# Get All Users from the database
def get_all_users_service():
    users = db.query(UserDB).all()
    user_details = []
    for user in users:
        user_dict = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "isAdmin": user.isAdmin
        }
        user_details.append(user_dict)
    return user_details

# Update User
def update_user(user_id: int, user: UserSchema):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete User
def delete_user(user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "User Deleted"}