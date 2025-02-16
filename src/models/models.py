from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.db import BaseModel


class User(BaseModel):
    email: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    phone: Mapped[str]

    snils: Mapped[str | None]
    group: Mapped[str | None]
    course: Mapped[int | None]

    # TODO: implement real passport fields
    passport_data: Mapped[str]


class Program(BaseModel):
    type: Mapped[str]
    priority: Mapped[int | None]
    okso: Mapped[str]
    profile: Mapped[str]
    form: Mapped[str | None]
    base: Mapped[str | None]
    sem_num: Mapped[int | None]
    university: Mapped[str]

    application_id: Mapped[int] = mapped_column(ForeignKey("application.id", ondelete="CASCADE"))


class Application(BaseModel):
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    hostel_policy_accepted: Mapped[bool]
    vacation_policy_viewed: Mapped[bool]
    no_restrictions_policy_accepted: Mapped[bool]
    reliable_information_policy_accepted: Mapped[bool]

    programs: Mapped[list[Program]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "application",
        "polymorphic_on": "type"
    }


class ReinstatementApplication(Application):
    """
    Восстановление
    """

    id: Mapped[int] = mapped_column(ForeignKey("application.id", ondelete="CASCADE"), primary_key=True)
    is_vacation_need: Mapped[bool]
    begin_year: Mapped[int]
    end_year: Mapped[int]
    purpose: Mapped[str]

    paid_policy_accepted: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": "reinstatement"
    }


class ChangeApplication(Application):
    """
    Изменение условий обучения
    """

    id: Mapped[int] = mapped_column(ForeignKey("application.id", ondelete="CASCADE"), primary_key=True)
    change_date: Mapped[datetime]
    purpose: Mapped[str] = mapped_column(String(1023))

    __mapper_args__ = {
        "polymorphic_identity": "change"
    }


class TransferApplication(Application):
    """
    Перевод из другого вуза
    """

    id: Mapped[int] = mapped_column(ForeignKey("application.id", ondelete="CASCADE"), primary_key=True)
    continue_year: Mapped[int | None]

    paid_policy_accepted: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": "transfer"
    }


class Documents(BaseModel):
    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
    type: Mapped[str]
    filepath: Mapped[str]
