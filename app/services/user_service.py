from app.errors.errors import UserNotFoundError, ValidationError, ConflictError, UnauthorizedError
from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str, email: str, password: str, role: str = "user") -> User:
        if not name:
            raise ValidationError("Name is required", field="name")
        if not email:
            raise ValidationError("Email is required", field="email")
        if not password:
            raise ValidationError("Password is required", field="password")
        if role not in ["user", "admin"]:
            raise ValidationError("Role must be 'user' or 'admin'", field="role")

        # Check if user with email already exists
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ConflictError("User with this email already exists", email=email)

        user = User(name=name, email=email, role=role)
        user.set_password(password)
        return self.repository.add(user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user by email and password"""
        user = self.repository.get_by_email(email)
        if user is None:
            raise UnauthorizedError("Invalid email or password")
        
        if not user.check_password(password):
            raise UnauthorizedError("Invalid email or password")
        
        return user

    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        user = self.repository.get_by_email(email)
        if user is None:
            raise UserNotFoundError(-1)  # Use -1 as placeholder since email is not ID
        return user
