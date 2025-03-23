from pydantic import BaseModel, Field
from datetime import datetime


class AdminApiTokenSchema(BaseModel):
    token: str


# const user = reactive({
#   email: "",
#   name: "",
#   surname: "",
#   patronymic: "",
#   phone: "",
#   snils: "",
#   course: null,
#   sex: null,
#   passport_data: {
#     seties: null,
#     sex: null,
#     birthdate: null,
#     birthplace: null,
#     issued_by: null,
#     issued_code: null,
#     issued_date: null,
#   },
# });


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
