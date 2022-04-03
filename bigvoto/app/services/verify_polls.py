from app.services.poll_service import PollService
from datetime import datetime

GMT = 3


async def veryfy(polls):
    poll_service = PollService()
    time_now = datetime.now().timestamp()

    for poll in polls:
        aux_start_date = datetime(poll['Poll'].start_date.year,
                                  poll['Poll'].start_date.month,
                                  poll['Poll'].start_date.day,
                                  poll['Poll'].start_date.hour + GMT,
                                  poll['Poll'].start_date.minute).timestamp()

        aux_end_date = datetime(poll['Poll'].end_date.year,
                                poll['Poll'].end_date.month,
                                poll['Poll'].end_date.day,
                                poll['Poll'].end_date.hour + GMT,
                                poll['Poll'].end_date.minute).timestamp()

        if aux_start_date <= time_now and aux_end_date >= time_now:
            await poll_service.active_polls(poll['Poll'].id, is_active=True)
        elif aux_start_date > time_now and aux_end_date >= time_now:
            await poll_service.active_polls(poll['Poll'].id, is_active=False)
        elif aux_end_date < time_now:
            await poll_service.active_polls(poll['Poll'].id, is_active=False)
        elif aux_end_date >= time_now and aux_start_date <= time_now:
            await poll_service.active_polls(poll['Poll'].id, is_active=True)
