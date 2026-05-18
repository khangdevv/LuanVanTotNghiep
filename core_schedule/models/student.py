import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from enums import Role

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Student(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    student_id: str = Field(min_length=1, max_length=20)
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    password_hash: str = Field(min_length=1, max_length=255)
    role: Role = Role.STUDENT
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not _EMAIL_RE.match(v):
            raise ValueError("email không đúng định dạng")
        return v
