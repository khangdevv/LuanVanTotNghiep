from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from enums import Role


class Student(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    student_id: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    password_hash: str = Field(min_length=1, max_length=255)
    role: Role = Role.STUDENT
    created_at: datetime = Field(default_factory=datetime.now)
