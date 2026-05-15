from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PersonalEvent(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    event_id: int
    student_id: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    day_of_week: Optional[int] = Field(default=None, ge=2, le=8)
    start_time: time
    end_time: time
    is_recurring: bool = False
    note: Optional[str] = None

    @model_validator(mode="after")
    def validate_time_range(self) -> "PersonalEvent":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        return self

