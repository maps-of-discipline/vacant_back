from enum import Enum


class PermissionsEnum(str, Enum):
    canCreateSelfApplication = "canCreateSelfApplication"
    canViewOwnApplications = "canViewOwnApplications"
    canCreateManySelfApplications = "canCreateManySelfApplications"

    canViewApplicationsList = "canViewApplicationsList"
    canChangeApplicationStatus = "canChangeApplicationStatus"

    canViewStuffComments = "canViewStuffComments"
    canCreateStuffComments = "canCreateStuffComments"
