from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class RegisterDTO(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6)
    role: Literal["user", "admin"] = Field(default="user")

