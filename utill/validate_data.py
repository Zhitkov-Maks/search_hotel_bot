from datetime import datetime


async def validate_date(dt):
    try:
        return datetime.strptime(dt, "%d-%m-%Y").date() >= datetime.today().date()
    except ValueError:
        return False


async def check_dt_1_less_date_2(dt1, dt2):
    return (
            datetime.strptime(dt1, "%d-%m-%Y").date()
            < datetime.strptime(dt2, "%d-%m-%Y").date()
    )
