import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY      = "YOUR_SECRET_KEY_HERE"
ALGORITHM       = "HS256"
MONGO_URI       = os.getenv('MONGO_URI')
DATABASE_NAME   = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client        = MongoClient(MONGO_URI)
db            = client[DATABASE_NAME] # type: ignore
collection    = db[COLLECTION_NAME] # type: ignore
pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    password: str
    private_token: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class Authentication:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def get_user(username: str):
        return collection.find_one({"username": username})

    @staticmethod
    def create_user(user: User) -> str:
        # Convert the Pydantic model to a dictionary and insert it into MongoDB
        user.password = Authentication.get_password_hash(user.password)
        # user.private_token = Authentication.get_password_hash(user.private_token)
        user_dict = user.model_dump()
        result = collection.insert_one(user_dict)
        # Return the string of the inserted_id
        return str(result.inserted_id)
    
    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        # Find a user in the MongoDB collection by _id
        return collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def update_user(user_id: str, user: User):
        # MongoDB: Update user data in the users collection by user_id
        update_data = user.model_dump(exclude_unset=True)
        collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    @staticmethod
    def delete_user(user_id: str):
        # MongoDB: Delete a user from the users collection by user_id
        collection.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    async def register(user: User):
        db_user = Authentication.get_user(user.username)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        Authentication.create_user(user)
        return {"username": user.username, "private_token": user.private_token}

    @staticmethod
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = Authentication.get_user(form_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        if not Authentication.verify_password(form_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Authentication.create_access_token(
            data={"sub": form_data.username, "private_token": user["private_token"]}, 
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except jwt.PyJWTError:
            raise credentials_exception
        user = Authentication.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
