from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Course(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    course_id: str = Field(min_length=1, max_length=20)
    course_name: str = Field(min_length=1, max_length=200)
    credits: int = Field(gt=0)
    department: Optional[str] = Field(default=None, max_length=100)
