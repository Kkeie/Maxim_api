from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BaseModelExtra(BaseModel):
    model_config = ConfigDict(extra="allow")


class Constituent(BaseModelExtra):
    constituentID: int | None = None
    role: str | None = None
    name: str | None = None


class Tag(BaseModelExtra):
    term: str | None = None
    AAT_URL: str | None = None
    Wikidata_URL: str | None = None


class SearchResponse(BaseModelExtra):
    """Список идентификаторов произведений, найденных поиском."""

    total: int
    objectIDs: list[int] = Field(default_factory=list)

    @field_validator("objectIDs", mode="before")
    @classmethod
    def normalize_object_ids(cls, value: list[int] | None) -> list[int]:
        return value or []


class ObjectResponse(BaseModelExtra):
    """Произведение искусства из коллекции Met Museum."""

    objectID: int
    title: str | None = None
    artistDisplayName: str | None = None
    artistDisplayBio: str | None = None
    objectDate: str | None = None
    objectBeginDate: int | None = None
    objectEndDate: int | None = None
    department: str | None = None
    medium: str | None = None
    classification: str | None = None
    culture: str | None = None
    period: str | None = None
    isHighlight: bool | None = None
    isPublicDomain: bool | None = None
    primaryImage: str | None = None
    objectURL: str | None = None
    constituents: list[Constituent] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)

    @field_validator("constituents", "tags", mode="before")
    @classmethod
    def normalize_lists(cls, value: list | None) -> list:
        return value or []
