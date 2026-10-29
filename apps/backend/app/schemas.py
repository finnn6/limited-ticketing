from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    total_quantity: int = Field(gt=0)
    per_user_limit: int = Field(default=1, ge=1)
    open_at: datetime
    close_at: datetime

    @model_validator(mode="after")
    def check_period(self):
        if self.close_at <= self.open_at:
            raise ValueError("마감 시각은 오픈 시각보다 늦어야 합니다")
        return self


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    total_quantity: int
    remaining_quantity: int
    per_user_limit: int
    open_at: datetime
    close_at: datetime

    
class IssueRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=50)


class IssueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    user_id: str