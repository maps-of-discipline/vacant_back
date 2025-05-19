from typing import Optional
from pydantic import BaseModel, Field

from src.models.models import Discipline


class GetRupDataAup(BaseModel):
    num: str
    sem: int


class GetRupDataSchema(BaseModel):
    source: GetRupDataAup
    target: GetRupDataAup


class ChoosenValueSchema(BaseModel):
    period: int
    variants: dict[str, bool]


class RupDiscipline(BaseModel):
    id: int
    title: str
    period: int
    zet: float
    control: str
    coursework: bool
    amount: float
    elective_group: int | None = Field(default=None)
    similarity: Optional[float] = Field(default=None)

    variants: list["RupDiscipline"] = Field(default_factory=list)

    @classmethod
    def from_model(
        cls, model: Discipline, serialize_variants: bool = False
    ) -> "RupDiscipline":
        instance = cls(
            id=model.id,
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
        if serialize_variants and model.variant_associations:
            for assoc in model.variant_associations:
                instance.variants.append(cls.from_model(assoc.variant, False))

        return instance


class BestMatchValue(BaseModel):
    target: str
    similarity: float


class GetRupDataResponseSchema(BaseModel):
    source: list[RupDiscipline]
    target: list[RupDiscipline]
    same: list[RupDiscipline]
    similar: list[RupDiscipline]
    best_match: dict[str, BestMatchValue]
    choosen: dict[str, ChoosenValueSchema]


class SetChoosenRequestSchema(BaseModel):
    target_id: int
    variant_id: int
    value: bool
