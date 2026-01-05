from pydantic import BaseModel, Field, EmailStr

class UserDTO(BaseModel):
    id: int
    name: str = Field(min_length=1)
    email: EmailStr
    role: str = Field(default="user")

    class Config:
        from_attributes = True  # SQLAlchemy support
