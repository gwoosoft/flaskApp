class AppError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message: str, **details):
        super().__init__(message)
        self.message = message
        self.details = details

class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"

class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"

class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class ValidationError(AppError):
    status_code = 400
    code = "validation_error"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"

class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: int):
        super().__init__("User not found", user_id=user_id)
