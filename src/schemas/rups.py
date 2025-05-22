from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from src.models.models import Discipline
from src.logger import get_logger

logger = get_logger(__name__)


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

    @classmethod
    def from_model(cls, model: Discipline) -> "RupDiscipline":
        instance = cls(
            id=model.id,
            title=model.title,
            period=model.period,
            zet=model.zet,
            control=model.control,
            coursework=model.coursework,
            amount=model.amount,
            elective_group=model.elective_group,
        )

        return instance


class RupDisciplineVariant(RupDiscipline):
    similarity: Optional[float] = Field(default=None)

    @classmethod
    def from_model(
        cls,
        model: Discipline,
        similarity: float = 0.0,
    ) -> "RupDisciplineVariant":
        instance = super().from_model(model)
        instance = cls(**instance.model_dump())
        instance.similarity = similarity

        return instance


class RupSameDiscipline(RupDiscipline):
    variants: list[RupDisciplineVariant] = Field(default_factory=list)

    @classmethod
    def from_model(
        cls,
        model: Discipline,
    ) -> "RupSameDiscipline":
        instance = super().from_model(model)
        instance = cls(**instance.model_dump())

        if model.variants:
            for assoc in model.variants:
                variant = RupDisciplineVariant.from_model(
                    assoc.variant, similarity=assoc.similarity
                )
                instance.variants.append(variant)

        return instance


class BestMatchValue(BaseModel):
    target: str
    similarity: float


class GetRupDataResponseSchema(BaseModel):
    source: list[RupDiscipline]
    target: list[RupDiscipline]
    same: list[RupDiscipline]
    similar: list[RupSameDiscipline]
    best_match: dict[str, BestMatchValue]
    choosen: dict[str, ChoosenValueSchema]


class SetChoosenRequestSchema(BaseModel):
    target_id: int
    variant_id: int
    value: bool
