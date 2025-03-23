from datetime import datetime

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.db import BaseModel


class User(BaseModel):
    external_id: Mapped[str] = mapped_column(unique=True)
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

    roles: Mapped[list["Role"]] = relationship(secondary="user_has_role")
    applications: Mapped["Application"] = relationship()


class Token(BaseModel):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user_agent: Mapped[str]
    token: Mapped[str]
    exp: Mapped[int]


class Role(BaseModel):
    external_id: Mapped[str]
    title: Mapped[str]

    users: Mapped[list[User]] = relationship(secondary="user_has_role")
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_has_permission"
    )


class Permission(BaseModel):
    title: Mapped[str]


user_has_role = Table(
    "user_has_role",
    BaseModel.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE")),
    Column("role_id", ForeignKey("role.id", ondelete="CASCADE")),
)


role_has_permission = Table(
    "role_has_permission",
    BaseModel.metadata,
    Column("role_id", ForeignKey("role.id", ondelete="CASCADE")),
    Column("permission_id", ForeignKey("permission.id", ondelete="CASCADE")),
)


class Program(BaseModel):
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
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    hostel_policy_accepted: Mapped[bool]
    vacation_policy_viewed: Mapped[bool]
    no_restrictions_policy_accepted: Mapped[bool]
    reliable_information_policy_accepted: Mapped[bool]

    programs: Mapped[list[Program]] = relationship(lazy="selectin")

    user: Mapped[User] = relationship()

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
    application_id: Mapped[int] = mapped_column(
        ForeignKey("application.id", ondelete="CASCADE")
    )
    type: Mapped[str]
    filepath: Mapped[str]
