from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Semester(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    semester_id: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    start_date: date
    end_date: date
    is_active: bool = False

    @model_validator(mode="after")
    def validate_dates(self) -> "Semester":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be greater than start_date")
        return self

