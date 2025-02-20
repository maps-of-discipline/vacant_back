from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str
    shils: str | None
    group: str | None
    course: str | None
    passport_data: str | None


class UserForListViewSchema(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str
    group: str | None
    course: int | None


class UserSchema(UserForListViewSchema):
    shils: str | None
    passport_data: str | None
