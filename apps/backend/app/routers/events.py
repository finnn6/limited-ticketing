from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.schemas import EventCreate, EventResponse

router = APIRouter()


@router.post("/admin/events", response_model=EventResponse, status_code=201)
def create_event(body: EventCreate, db: Session = Depends(get_db)):
    event = Event(**body.model_dump(), remaining_quantity=body.total_quantity)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다")
    return event