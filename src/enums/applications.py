from enum import Enum


class ApplicationStatusEnum(str, Enum):
    new = "new"
    in_progres = "in progres"
    approved = "approved"
    rejected = "rejected"
