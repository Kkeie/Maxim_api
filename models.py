from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class BaseModelExtra(BaseModel):
    model_config = ConfigDict(extra="allow")


class SearchResponse(BaseModelExtra):
    total: int
    objectIDs: list[int] = Field(default_factory=list)


class ObjectResponse(BaseModelExtra):
    objectID: int
    title: str | None = None
    artistDisplayName: str | None = None


class DepartmentItem(BaseModelExtra):
    departmentId: int
    displayName: str


class DepartmentsResponse(BaseModelExtra):
    departments: list[DepartmentItem] = Field(default_factory=list)
