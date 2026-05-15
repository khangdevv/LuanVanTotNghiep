from pydantic import BaseModel, ConfigDict, Field


class ScheduleClass(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    schedule_id: int
    class_id: str = Field(min_length=1, max_length=20)
