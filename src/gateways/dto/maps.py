from typing import Optional

from pydantic import BaseModel, Field


class RupDiscipline(BaseModel):
    title: str
    period: int
    zet: float
    control: str
    coursework: bool
    amount: float
    elective_group: int | None = Field(default=None)
    similarity: Optional[float] = Field(default=None)

    variants: list["RupDiscipline"] = Field(default_factory=list)


class BestMatchValue(BaseModel):
    target: str
    similarity: float


class RupData(BaseModel):
    source: list[RupDiscipline]
    target: list[RupDiscipline]
    same: list[RupDiscipline]
    similar: list[RupDiscipline]
    best_match: dict[str, BestMatchValue]
