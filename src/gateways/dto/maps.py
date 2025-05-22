from typing import Optional

from pydantic import BaseModel, Field

from src.models.models import Discipline


class MapsRupDiscipline(BaseModel):
    title: str
    period: int
    zet: float
    control: str
    coursework: bool
    amount: float
    elective_group: int | None = Field(default=None)
    similarity: Optional[float] = Field(default=None)

    variants: list["MapsRupDiscipline"] = Field(default_factory=list)

    @classmethod
    def from_model(
        cls, model: Discipline, serialize_variants: bool = False
    ) -> "MapsRupDiscipline":
        instance = cls(
            title=model.title,
            period=model.period,
            zet=model.zet,
            control=model.control,
            coursework=model.coursework,
            amount=model.amount,
            elective_group=model.elective_group,
            similarity=None,
            variants=[],
        )
        if serialize_variants and model.variants:
            for assoc in model.variants:
                instance.variants.append(cls.from_model(assoc.variant, False))

        return instance


class BestMatchValue(BaseModel):
    target: str
    similarity: float


class RupData(BaseModel):
    source: list[MapsRupDiscipline]
    target: list[MapsRupDiscipline]
    same: list[MapsRupDiscipline]
    similar: list[MapsRupDiscipline]
    best_match: dict[str, BestMatchValue]
