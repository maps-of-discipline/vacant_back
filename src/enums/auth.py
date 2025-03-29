from enum import Enum


class PermissionsEnum(str, Enum):
    canCreateSelfApplication = "canCreateSelfApplication"
    canViewOwnApplications = "canViewOwnApplications"
    canCreateManySelfApplications = "canCreateManySelfApplications"
    canDoSomething2 = "canDoSomething2"
