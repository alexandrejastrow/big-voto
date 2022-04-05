from app.security.auth import get_user_token
from app.services.poll_service import PollService, AlternativeService
from app.schemas.schemas import AlternativeCreate, PollCreate, User
from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, BackgroundTasks, Security, HTTPException, status
from app.settings.settings import app_settings
from app.services import queue_sender

DEFAULT_MAX_TIME_TO_POLL = app_settings.DEFAULT_MAX_TIME_TO_POLL
TIMESTAMP_TOLEANCE = 60
INTERVAL_SECONDS = 10
GMT = 3
poll_router = APIRouter(tags=["Poll"])


@poll_router.post("/")
async def create_poll(poll: PollCreate, alternatives: List[AlternativeCreate], user: User = Security(get_user_token)):
    end_date = None
    start_date = None

    time_now = (datetime.now() - timedelta(hours=GMT)
                ).replace(tzinfo=timezone.utc).timestamp()

    if poll.end_date is None:
        end_date = (datetime.now() - timedelta(hours=GMT)) + \
            timedelta(minutes=DEFAULT_MAX_TIME_TO_POLL)
    else:
        aux_end_date = datetime(poll.end_date.year,
                                poll.end_date.month,
                                poll.end_date.day,
                                poll.end_date.hour,
                                poll.end_date.minute,
                                poll.end_date.second
                                ).timestamp()

        if aux_end_date <= time_now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="End date must be in the future")
        end_date = datetime(poll.end_date.year,
                            poll.end_date.month,
                            poll.end_date.day,
                            poll.end_date.hour,
                            poll.end_date.minute,
                            poll.end_date.second)
    is_active = False

    if poll.start_date is None:
        start_date = (datetime.now() - timedelta(hours=GMT))
        is_active = True
    else:
        aux_start_date = datetime(poll.start_date.year,
                                  poll.start_date.month,
                                  poll.start_date.day,
                                  poll.start_date.hour,
                                  poll.start_date.minute,
                                  poll.start_date.second).timestamp()

        if aux_start_date < time_now - TIMESTAMP_TOLEANCE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="start date must be in the future")

        start_date = datetime(poll.start_date.year,
                              poll.start_date.month,
                              poll.start_date.day,
                              poll.start_date.hour,
                              poll.start_date.minute,
                              poll.start_date.second)

    if end_date <= start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="End date must be greater than start date")

    poll_service = PollService()
    poll.end_date = end_date
    poll.start_date = start_date

    poll_db = await poll_service.create(poll, author_id=user.id, is_active=is_active)

    if not poll_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "detail": "Fail to create poll."})
    alternative_service = AlternativeService()

    alternative_db = []
    for alternative in alternatives:
        alternative_db.append(await alternative_service.create(alternative, poll_db.id))

        if not alternative_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                "detail": "Fail to create alternative."})

    return {"poll": poll_db, "alternatives": alternative_db}


@poll_router.get("/")
async def get_all_polls():
    poll_service = PollService()
    alternative_service = AlternativeService()
    polls = await poll_service.get_all()

    for poll in polls:
        poll["alternatives"] = await alternative_service.get_all(poll['Poll'].id)
    return polls


@poll_router.get("/active")
async def get_all_active_polls():
    poll_service = PollService()
    alternative_service = AlternativeService()
    polls = await poll_service.get_all(is_active=True)
    for poll in polls:
        poll["alternatives"] = await alternative_service.get_all(poll['Poll'].id)
    return polls


@poll_router.get("/deactivated")
async def get_all_deactivated_polls():
    poll_service = PollService()
    alternative_service = AlternativeService()
    polls = await poll_service.get_all(is_active=False)
    for poll in polls:
        poll["alternatives"] = await alternative_service.get_all(poll['Poll'].id)
    return polls


@poll_router.get("/{poll_id}/{alternative_id}")
async def vote(poll_id: str, alternative_id: str, task: BackgroundTasks):

    poll_service = PollService()
    polls = await poll_service.get_by_id(poll_id)

    if polls["Poll"].is_active:
        task.add_task(queue_sender.send_message, {
                      "alternative_id": alternative_id})
        return {"message": "Vote sent to queue"}
    else:
        return {"message": "Poll is not active"}
