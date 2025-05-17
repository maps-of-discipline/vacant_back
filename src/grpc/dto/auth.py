from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenPayload:
    user_id: str
    role: str
    expires_at: str
    service_name: str
    permissions: list[str]


@dataclass
class UserData:
    id: str
    external_id: str
    role: str
    external_role: str
    name: str
    surname: str
    patronymic: str
    email: str
    faculty: str
    login: str
    last_login: str
    created_at: str
    sex: str
    study_status: str
    degree_level: str
    study_group: str
    specialization: str
    finance: str
    form: str
    enter_year: str
    course: str
