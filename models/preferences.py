from pydantic import BaseModel, ConfigDict, Field, model_validator

from enums import PreferredSlot


class Preference(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    student_id: str = Field(min_length=1, max_length=20)
    preferred_slot: PreferredSlot = PreferredSlot.MORNING
    min_break_minutes: int = Field(default=15, ge=0)
    w_break: float = Field(default=0.40, ge=0, le=1)
    w_preference: float = Field(default=0.30, ge=0, le=1)
    w_balance: float = Field(default=0.30, ge=0, le=1)

    @model_validator(mode="after")
    def validate_weights(self) -> "Preference":
        weights = (self.w_break, self.w_preference, self.w_balance)
        if abs(sum(weights) - 1.0) > 1e-9:
            raise ValueError("w_break + w_preference + w_balance must equal 1.0")
        return self
