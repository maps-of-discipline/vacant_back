from fastapi import HTTPException


class ItemNotFoundException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=400, detail=detail)


class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str) -> None:
        super().__init__(f"{entity_name} not found!")
