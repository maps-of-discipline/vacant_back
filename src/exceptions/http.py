from fastapi.exceptions import HTTPException


class NoUserAgentException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User agent header must be in reqeust")


class EntityAlreadyExistsHTTPException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(400, detail)


class EntityNotFoundHTTPException(HTTPException):
    def __init__(self, entity: str):
        super().__init__(400, f"{entity} not found!")
