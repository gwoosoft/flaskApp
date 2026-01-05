from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    id: int
    name: str = Field(min_length=1)

    class Config:
        from_attributes = True  # SQLAlchemy support
