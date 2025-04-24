from datetime import datetime

from sqlalchemy import String, ForeignKey, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.db import BaseModel


class User(BaseModel):
    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    phone: Mapped[str | None]

    snils: Mapped[str | None]
    group: Mapped[str | None]
    course: Mapped[int | None]

    sex: Mapped[str]
    birtdate: Mapped[datetime]
    passport_series: Mapped[str]
    passport_birthplace: Mapped[str]
    passport_issued_by: Mapped[str]
    passport_issued_code: Mapped[str]
    passport_issued_date: Mapped[datetime]

    applications: Mapped["Application"] = relationship()

    @property
    def fullname(self) -> str:
        return f"{self.surname} {self.name} {self.patronymic}"


class Program(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    okso: Mapped[str]
    profile: Mapped[str]
    form: Mapped[str | None]
    base: Mapped[str | None]
    sem_num: Mapped[int | None]
    university: Mapped[str]

    application_id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE")
    )


class Application(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[str]
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    hostel_policy_accepted: Mapped[bool]
    vacation_policy_viewed: Mapped[bool]
    no_restrictions_policy_accepted: Mapped[bool]
    reliable_information_policy_accepted: Mapped[bool]

    programs: Mapped[list[Program]] = relationship(lazy="selectin")

    user: Mapped[User] = relationship()

    status: Mapped["Status"] = relationship(
        "Status", primaryjoin="Status.id == Application.status_id"
    )

    __mapper_args__ = {"polymorphic_identity": "application", "polymorphic_on": "type"}


class ReinstatementApplication(Application):
    """
    Восстановление
    """

    id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE"), primary_key=True
    )
    is_vacation_need: Mapped[bool]
    begin_year: Mapped[int]
    end_year: Mapped[int]
    purpose: Mapped[str]

    paid_policy_accepted: Mapped[bool]

    __mapper_args__ = {"polymorphic_identity": "reinstatement"}


class ChangeApplication(Application):
    """
    Изменение условий обучения
    """

    id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE"), primary_key=True
    )
    purpose: Mapped[str] = mapped_column(String(1023))

    __mapper_args__ = {"polymorphic_identity": "change"}


class TransferApplication(Application):
    """
    Перевод из другого вуза
    """

    id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE"), primary_key=True
    )
    continue_year: Mapped[int | None]

    paid_policy_accepted: Mapped[bool]

    __mapper_args__ = {"polymorphic_identity": "transfer"}


class Documents(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE")
    )
    type: Mapped[str]
    filepath: Mapped[str]


class Status(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    verbose_name: Mapped[str]


class CommonMessages(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id", ondelete="CASCADE"))
    title: Mapped[str]


class Comment(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    scope: Mapped[str]
    application_id = mapped_column(ForeignKey("application.id", ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship()
