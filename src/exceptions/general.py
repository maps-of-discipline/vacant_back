from fastapi import HTTPException


class ItemNotFoundException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=400, detail=detail)


class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str) -> None:
        super().__init__(f"{entity_name} not found!")
        self.entity = entity_name


class EntityAlreadyExists(Exception):
    def __init__(self, entity_name):
        super().__init__(f"{entity_name} already exists!")
        self.entity = entity_name
