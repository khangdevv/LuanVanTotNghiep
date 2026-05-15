from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Schedule(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    schedule_id: int
    student_id: str = Field(min_length=1, max_length=20)
    semester_id: str = Field(min_length=1, max_length=10)
    score_total: float = Field(ge=0, le=1)
    score_break: float = Field(ge=0, le=1)
    score_pref: float = Field(ge=0, le=1)
    score_balance: float = Field(ge=0, le=1)
    is_selected: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
