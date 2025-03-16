from fastapi.exceptions import HTTPException


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(401, f"Authorization token in invalid. {detail}")


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(401, "Authorization token has expired")


class AdminApiTokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(401, "AdminApi token has expired")


class PermissionsDeniedException(HTTPException):
    def __init__(self):
        super().__init__(403, "User don't have access permissions")
