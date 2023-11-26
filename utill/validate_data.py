from datetime import datetime


async def validate_date(dt) -> bool:
    """Проверяем валидность введенной даты."""
    try:
        return datetime.strptime(dt, "%d-%m-%Y").date() >= datetime.today().date()
    except ValueError:
        return False


async def check_dt_1_less_date_2(dt1, dt2) -> int | bool:
    """Проверяем чтобы дата выезда была больше даты заезда."""
    try:
        if (
            datetime.strptime(dt1, "%d-%m-%Y").date()
            < datetime.strptime(dt2, "%d-%m-%Y").date()
        ):
            return (
                    datetime.strptime(dt2, "%d-%m-%Y").date()
                    - datetime.strptime(dt1, "%d-%m-%Y").date()
            ).days
        else:
            return False
    except ValueError:
        return False


async def check_data_digit(digit: str) -> bool:
    """Проверяем введено ли целое число."""
    if not digit.isdigit():
        return False
    return True


async def check_price_data(pr_min: int, pr_max: int) -> bool:
    """Проверка цены на валидность."""
    return pr_max > pr_min
