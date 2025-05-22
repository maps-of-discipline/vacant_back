from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CreateUserSchema(BaseModel):
    email: str
    name: str
    surname: str
    patronymic: str
    type_: str

    phone: str | None
    snils: str | None

    birtdate: datetime = Field(default_factory=datetime.now)

    passport_series: str = Field(default="None")
    passport_number: str = Field(default="None")

    passport_birthplace: str = Field(default="None")
    passport_issued_by: str = Field(default="None")
    passport_issued_code: str = Field(default="None")
    passport_issued_date: datetime = Field(default_factory=datetime.now)

    sex: Optional[str]
    study_status: Optional[str]
    degree_level: Optional[str]
    study_group: Optional[str]
    specialization: Optional[str]
    finance: Optional[str]
    form: Optional[str]
    enter_year: Optional[str]
    course: Optional[str]

    send_email: bool = Field(default=True)


class UserSchema(CreateUserSchema):
    id: str

    @property
    def fullname(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"

    @property
    def shotname(self) -> str:
        return f"{self.surname} {self.name[0]}.{self.patronymic[0]}."


class UserForListViewSchema(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    patronymic: str
    phone: str | None
    group: str | None
    course: int | None
