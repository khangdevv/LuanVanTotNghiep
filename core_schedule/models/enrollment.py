from pydantic import BaseModel, ConfigDict, Field


class Enrollment(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    enrollment_id: int
    student_id: str = Field(min_length=1, max_length=20)
    course_id: str = Field(min_length=1, max_length=20)
    semester_id: str = Field(min_length=1, max_length=10)
