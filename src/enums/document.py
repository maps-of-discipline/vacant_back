from enum import Enum


class DocumnetTypeEnum(str, Enum):
    passport = "passport"
    recordBook = "recordBook"
    statusDocument = "statusDocument"
    studyPeriod = "studyPeriod"
    consent = "consent"
    achievements = "achievements"