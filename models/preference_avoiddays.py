from pydantic import BaseModel, Field


class PreferenceAvoidDay(BaseModel):
    pref_id: int
    day_of_week: int = Field(ge=2, le=8)
