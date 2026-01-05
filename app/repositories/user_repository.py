from app.models.user import User
from app.extensions import db

class UserRepository:
    def add(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id: int) -> User:
        return db.session.get(User, user_id)
