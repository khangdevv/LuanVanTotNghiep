from pydantic import BaseModel, ConfigDict, Field


class PreferenceAvoidDay(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    pref_id: int
    day_of_week: int = Field(ge=2, le=8)
