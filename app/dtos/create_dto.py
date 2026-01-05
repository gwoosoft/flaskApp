from pydantic import BaseModel, Field

class CreateUserDTO(BaseModel):
    name: str = Field(min_length=1)
