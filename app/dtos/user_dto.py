from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # SQLAlchemy support
