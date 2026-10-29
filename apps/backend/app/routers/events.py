from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.database import get_db
from app.models import Event, Issuance
from app.schemas import EventCreate, EventResponse, IssueRequest, IssueResponse

from datetime import datetime


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

@router.post("/events/{event_id}/issue", response_model=IssueResponse, status_code=201)
def issue(event_id: int, body: IssueRequest, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다")

    now = datetime.now()
    if now < event.open_at:
        raise HTTPException(status_code=400, detail="오픈 전입니다")
    if now > event.close_at:
        raise HTTPException(status_code=400, detail="마감 시각이 지났습니다")

    issued_count = db.scalar(
        select(func.count())
        .select_from(Issuance)
        .where(Issuance.event_id == event_id, Issuance.user_id == body.user_id)
    )
    
    if issued_count >= event.per_user_limit:
        raise HTTPException(status_code=409, detail="이미 발급받았습니다")

    if event.remaining_quantity <= 0:
        raise HTTPException(status_code=409, detail="수량이 소진되었습니다")

    # 문제 지점: 조회한 값을 파이썬에서 빼서 다시 저장 (read-modify-write)
    event.remaining_quantity -= 1
    issuance = Issuance(event_id=event_id, user_id=body.user_id)
    db.add(issuance)
    db.commit()
    db.refresh(issuance)
    return issuance