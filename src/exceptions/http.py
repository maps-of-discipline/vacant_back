from fastapi.exceptions import HTTPException


class NoUserAgenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User agent header must be in reqeust")
