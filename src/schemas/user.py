from pydantic import BaseModel, Field
from datetime import datetime



class CreateUserSchema(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str | None
    snils: str | None
    group: str | None = Field(default=None)
    course: int | None

    sex: str = Field(default="None")
    birtdate: datetime = Field(default_factory=datetime.now)
    passport_series: str = Field(default="None")

    passport_birthplace: str = Field(default="None")
    passport_issued_by: str = Field(default="None")
    passport_issued_code: str = Field(default="None")
    passport_issued_date: datetime = Field(default_factory=datetime.now)


class UserSchema(CreateUserSchema):
    id: str


class UserForListViewSchema(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str | None
    group: str | None
    course: int | None
