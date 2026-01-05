from app.dtos.user_dto import UserDTO
from app.dtos.login_dto import LoginDTO
from app.dtos.register_dto import RegisterDTO
from app.services.user_service import UserService

class UserFacade:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(self, user_id: int) -> dict:
        user = self.user_service.get_user(user_id)
        return UserDTO.model_validate(user).model_dump()

    def register_user(self, payload: dict) -> dict:
        """Register a new user (public endpoint) - role defaults to 'user'"""
        dto = RegisterDTO.model_validate(payload)
        # Only allow 'user' role for public registration (prevent self-promotion to admin)
        role = "user" if dto.role == "admin" else dto.role
        user = self.user_service.create_user(dto.name, dto.email, dto.password, role)
        return UserDTO.model_validate(user).model_dump()

    def create_user(self, payload: dict) -> dict:
        """Create a user (admin-only endpoint) - allows setting any role"""
        dto = RegisterDTO.model_validate(payload)
        user = self.user_service.create_user(dto.name, dto.email, dto.password, dto.role)
        return UserDTO.model_validate(user).model_dump()

    def authenticate_user(self, payload: dict) -> dict:
        """Authenticate a user and return user info"""
        dto = LoginDTO.model_validate(payload)
        user = self.user_service.authenticate_user(dto.email, dto.password)
        return UserDTO.model_validate(user).model_dump()
