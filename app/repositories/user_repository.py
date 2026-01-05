from typing import Optional
from app.models.user import User
from app.extensions import db
from sqlalchemy import select

class UserRepository:
    def add(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id: int) -> Optional[User]:
        return db.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.session.scalar(stmt)
