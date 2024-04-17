# main.py
from fastapi import FastAPI, HTTPException, Depends
from .routes.user import user_routes
from .routes.services import service_routes
from .db.db_setup import engine, Base
from sqlalchemy.orm import sessionmaker
from fastapi.templating import Jinja2Templates
from .models.models import User, chatPrompts, chatResponses
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .settings.configurations import create_access_token
from .services.user_queries import authenticate_user
from jinja2 import Environment, FileSystemLoader

app = FastAPI()
app.include_router(user_routes)
app.include_router(service_routes)

# Setup these User, chatPrompts and chatResponses table with the database
Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure Jinja2 environment
templates = Jinja2Templates(directory="templates")

# Configure Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

# Root route
@app.get("/")
def root():
    return {"message": "hello world!"}

# OAuth2 token route
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
