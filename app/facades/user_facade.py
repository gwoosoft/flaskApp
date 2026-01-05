from app.dtos.create_dto import CreateUserDTO
from app.dtos.user_dto import UserDTO
from app.services.user_service import UserService

class UserFacade:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, payload: dict) -> dict:
        dto = CreateUserDTO.model_validate(payload)
        user = self.user_service.create_user(dto.name)
        return UserDTO.model_validate(user).model_dump()

    def get_user(self, user_id: int) -> dict:
        user = self.user_service.get_user(user_id)
        return UserDTO.model_validate(user).model_dump()
