from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Header, status, Query
from datetime import datetime, timedelta
from userModel import User, JwtInfo
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from fastapi.middleware.cors import CORSMiddleware

import jwt
import random
import os
import httpx

import userModel

app = FastAPI()

load_dotenv()
uri = os.getenv('MONGODB_URI')

# Create a new client and connect to the server
client = MongoClient(uri)

# Set the desired db
db = client.parcial

versionRoute = "api"

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"API": "REST"}


@app.post("/" + versionRoute + "/auth/jwt")
async def generate_jwt_token(account: JwtInfo):
    user_found = db.User.find_one({"email": account.email})
    id = None
    if user_found is None:
        username_suffix = '#' + ''.join((random.choice('abcdxyzpqr') for _ in range(5)))
        user_found = db.User.insert_one(User(username=account.username + username_suffix, email=account.email).model_dump(by_alias=True, exclude=["id"]))
        id = str(user_found.inserted_id)
    else:
        id = str(user_found['_id'])
    payload = {
        "sub": id,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    jwt_token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")

    return JSONResponse(content=jsonable_encoder({"jwt": jwt_token, "id": id}))


@app.get("/" + versionRoute + "/users/",
         summary="Find a user list",
         response_description="Returns all the users",
         response_model=userModel.UserBasicInfoCollection,
         status_code=status.HTTP_200_OK,
         tags=["User"])
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(10, le=20)):
    skip = (page - 1) * page_size
    users = db.User.find(None, {"username": 1, "email": 1}).skip(skip).limit(page_size)
    return {"users": list(users)}
