from enum import Enum, StrEnum, auto


class PermissionsEnum(StrEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name

    canCreateUserComments = auto()

    # user
    canViewOwnApplications = auto()
    canViewUserComments = auto()
    canCreateSelfApplication = auto()
    canEditOwnApplications = auto()

    # stuff
    canViewApplicationsList = auto()
    canViewProcessApplication = auto()
    canViewDashboard = auto()
    canViewRups = auto()

    canChangeApplicationStatus = auto()
    canViewStuffComments = auto()
    canCreateStuffComments = auto()

    # debug
    canUpdateTokens = auto()
    canViewRefreshTokens = auto()
    canViewApplicationTypeChooseModel = auto()
