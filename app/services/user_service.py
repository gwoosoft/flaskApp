from app.errors.errors import UserNotFoundError, ValidationError
from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str) -> User:
        if not name:
            raise ValidationError("Name is required", field="name")

        user = User(name=name)
        return self.repository.add(user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
