from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.errors.errors import ForbiddenError
from app.repositories.user_repository import UserRepository


def admin_required(f):
    """Decorator to require admin role for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()  # Returns string, convert to int
        
        # Get user service to check role
        user_repo = UserRepository()
        user = user_repo.get(int(user_id))
        
        if user is None:
            raise ForbiddenError("User not found")
        
        if not user.is_admin():
            raise ForbiddenError("Admin access required")
        
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Helper function to get the current authenticated user"""
    user_id = get_jwt_identity()  # Returns string, convert to int
    user_repo = UserRepository()
    user = user_repo.get(int(user_id))
    
    if user is None:
        raise ForbiddenError("User not found")
    
    return user

