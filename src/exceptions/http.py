from fastapi.exceptions import HTTPException


class NoUserAgentException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User agent header must be in reqeust")
