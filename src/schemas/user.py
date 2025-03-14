from pydantic import BaseModel


class AdminApiTokenSchema(BaseModel):
    token: str


class CreateUserSchema(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str | None
    snils: str | None
    group: str | None
    course: int | None
    passport_data: str | None


class UserForListViewSchema(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str | None
    group: str | None
    course: int | None


class UserSchema(CreateUserSchema):
    id: int
    external_id: str

