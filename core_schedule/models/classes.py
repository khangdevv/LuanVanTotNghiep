from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class ClassSection(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    class_id: str = Field(min_length=1, max_length=20)
    course_id: str = Field(min_length=1, max_length=20)
    semester_id: str = Field(min_length=1, max_length=10)
    day_of_week: int = Field(ge=2, le=8)
    start_time: time
    end_time: time
    room: Optional[str] = Field(default=None, max_length=50)
    instructor: Optional[str] = Field(default=None, max_length=100)
    max_students: int = Field(default=1, gt=0)

    @model_validator(mode="after")
    def validate_time_range(self) -> "ClassSection":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be greater than start_time")
        return self

    @computed_field
    @property
    def duration_minutes(self) -> int:
        # Số phút của buổi học (tính từ start_time đến end_time)
        today = datetime.today()
        start = datetime.combine(today, self.start_time)
        end = datetime.combine(today, self.end_time)
        return int((end - start).total_seconds() // 60)

    @computed_field
    @property
    def day_of_week_label(self) -> str:
        # Tên thứ trong tuần (2 = Thứ Hai, ..., 8 = Chủ Nhật).
        labels = {2: "Thứ Hai", 3: "Thứ Ba", 4: "Thứ Tư", 5: "Thứ Năm",
                  6: "Thứ Sáu", 7: "Thứ Bảy", 8: "Chủ Nhật"}
        return labels.get(self.day_of_week, "Không xác định")


