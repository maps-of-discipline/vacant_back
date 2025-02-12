from db import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from datetime import datetime


class User(BaseModel):
    fullname: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(12))
    email: Mapped[str] = mapped_column(String(255))
    # TODO: implement real passport fields
    passport_data: Mapped[str]
    group: Mapped[str]
    course: Mapped[int]
    snils: Mapped[str]


class Program(BaseModel):
    type: Mapped[str]
    priority: Mapped[int]
    okso: Mapped[str]
    form: Mapped[str]
    base: Mapped[str]
    sem_num: Mapped[int]
    university: Mapped[str]

    application_id: Mapped["Application"] = mapped_column(ForeignKey("application.id"))


class Application(BaseModel):
    date: Mapped[datetime]
    type: Mapped[str]


class ReinsatatementApplication(BaseModel):
    """
    Восстановление
    """

    application_id: Mapped["Application"] = mapped_column(ForeignKey("application.id"))
    is_vacation_need: Mapped[bool]
    begin_year: Mapped[int]
    end_year: Mapped[int]
    okso: Mapped[str]
    program: Mapped[str]
    purpose: Mapped[str] = mapped_column(String(1023))


class ChangeApplication(BaseModel):
    """
    Изменение условий обучения
    """

    application_id: Mapped["Application"] = mapped_column(ForeignKey("application.id"))
    purpose: Mapped[str] = mapped_column(String(1023))


class TransferApplication(BaseModel):
    """
    Перевод из другого вуза
    """

    application_id: Mapped["Application"] = mapped_column(ForeignKey("application.id"))
    continue_year: Mapped[int]


class Documents(BaseModel):
    application_id: Mapped["Application"] = mapped_column(ForeignKey("application.id"))
    type: Mapped[str]
    title: Mapped[str]
    filepath: Mapped[str]
