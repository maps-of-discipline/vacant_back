from enum import Enum


class PermissionsEnum(str, Enum):
    perm1 = "perm1"
    perm2 = "perm2"
    canCreateSelfApplication = "canCreateSelfApplication"
    canViewOwnApplications = "canViewOwnApplications"
    canCreateManySelfApplications = "canCreateManySelfApplications"
