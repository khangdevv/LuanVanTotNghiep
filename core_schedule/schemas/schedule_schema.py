from __future__ import annotations


from pydantic import BaseModel, Field

from models.classes import ClassSection
from models.personal_events import PersonalEvent
from models.preferences import Preference

class GenerateScheduleRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=20)
    semester_id: str = Field(min_length=1, max_length=10)
    classes: list[ClassSection] = Field(min_length=1)
    preferences: Preference
    personal_events: list[PersonalEvent] = Field(default_factory=list)
    avoid_days: list[int] = Field(default_factory=list)
    max_solutions: int = Field(default=500, ge=1, le=5000)

class DetectConflictRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=20)
    semester_id: str = Field(min_length=1, max_length=10)
    classes: list[ClassSection] = Field(min_length=1)

class DetectConflictResponse(BaseModel):
    semester_id: str
    conflicts: list[tuple[ClassSection, ClassSection]] = Field(default_factory=list)
    total_conflicts: int = Field(ge=0)
    is_valid: bool

class ScheduleResult(BaseModel):
    rank: int = Field(ge=1)
    is_recommended: bool = Field(default=False)
    algorithm_tag: str = Field(default="CSP")
    classes: list[ClassSection]
    score_total: float = Field(ge=0, le=1)
    score_break: float = Field(ge=0, le=1)
    score_pref: float = Field(ge=0, le=1)
    score_balance: float = Field(ge=0, le=1)

class GenerateScheduleResponse(BaseModel):
    student_id: str
    semester_id: str
    total_found: int = Field(ge=0)
    schedules: list[ScheduleResult]
