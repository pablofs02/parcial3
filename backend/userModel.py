from bson import ObjectId
from pydantic import BeforeValidator, BaseModel, ConfigDict, EmailStr, Field
from typing_extensions import Annotated
from typing import List, Optional
import datetime
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class JwtInfo(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "name@email.com",
            }
        }
    )

class UserBasicInfo(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    username: str = Field(...)
    email: str = Field(...)

class UserBasicInfoCollection(BaseModel):
    users: List[UserBasicInfo]

class Product(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    title: str = Field(...)
    closeDate: datetime = Field(...)
    buyer: Optional[UserBasicInfo] = Field(None)

class ProductId(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)

class ProductBasicInfo(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    title: str = Field(...)

class ProductCollection(BaseModel):
    products: List[Product]

class Bid(BaseModel):
    id: str = Field(...)
    amount: float = Field(...)
    timestamp: datetime = Field(...)
    product: ProductBasicInfo = Field(...)

class Location(BaseModel):
    lat: float = Field(...)
    lon: float = Field(...)

class Rating(BaseModel):
    value: float = Field(...)
    product: ProductId = Field(...)
    timestamp: datetime = Field(...)
    user: UserBasicInfo = Field(...)

class User(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    username: str = Field(...)
    email: str = Field(None)

    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "ejemplo@gmail.com",
            }
        }
    )

class CreateUser(BaseModel):
    id: PyObjectId = Field(default=None, alias="_id")
    username: str = Field(...)
    email: str = Field(...)
    location: Location = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "username",
                "location": {
                    "lat": 36.749058,
                    "lon": -4.516260
                },
            }
        }
    )

class UpdateUser(BaseModel):
    username: Optional[str] = Field(None)
    location: Optional[Location] = Field(None)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "username",
                "location": {
                    "lat": 36.749058,
                    "lon": -4.516260
                }
            }
        }
    )
