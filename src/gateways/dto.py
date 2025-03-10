import json
from httpx import Response
from dataclasses import dataclass


@dataclass
class AdminApiUser:
    id: str
    external_id: int
    role: str
    external_role: str
    name: str
    surname: str
    patronymic: str
    email: str
    login: str

    @staticmethod
    def from_response(response: Response) -> "AdminApiUser":
        user_data = json.loads(response.json())
        return AdminApiUser(
            id=user_data["id"],
            external_id=user_data["external_id"],
            role=user_data["role"],
            external_role=user_data["external_role"],
            name=user_data["name"],
            surname=user_data["surname"],
            patronymic=user_data["patronymic"],
            email=user_data["email"],
            login=user_data["login"],
        )


@dataclass
class AdminApiServiceRole:
    id: str
    service_id: str
    role: str


@dataclass
class AdminApiUserServiceRole:
    id: str
    service_role_id: str
    user_id: str
