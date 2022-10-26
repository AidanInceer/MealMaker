
import calendar
from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass
class HomePageCalender:

    @staticmethod
    def generate_calendar_object() -> dict:
        # Object preparation
        now = datetime.now()
        week_start_date = now - timedelta(days=now.weekday())
        week_end_date = week_start_date + timedelta(days=6)
        today = date.today()
        no_days_curr_month = calendar.monthrange(datetime.now().year, datetime.now().month)[
            1
        ]
        previous_month_word = (date.today().replace(day=1) - timedelta(days=1)).strftime(
            "%B"
        )
        starting_weekday = datetime(today.year, today.month, 1).weekday()
        end_weekday = datetime(today.year, today.month, no_days_curr_month).weekday()
        no_days_previous_month = calendar.monthrange(
            datetime.now().year, datetime.now().month - 1
        )[1]

        previous_month_list = [x + 1 for x in range(no_days_previous_month)][
            -starting_weekday:
        ]
        current_month_list = [x + 1 for x in range(no_days_curr_month)]
        next_month_list = [x + 1 for x in range((7 - 1 - end_weekday))]

        # Calendar object
        calendar_data = {
            "current_day": datetime.now().day,
            "current_weekday": datetime.now().strftime("%A"),
            "week_start_day": week_start_date.day,
            "week_end_day": week_end_date.day,
            "current_month_int": datetime.now().month,
            "current_month_word": datetime.now().strftime("%B"),
            "previous_month_word": previous_month_word,
            "no_days_curr_month": no_days_curr_month,
            "no_days_previous_month": no_days_previous_month,
            "previous_month_list": previous_month_list,
            "current_month_list": current_month_list,
            "next_month_list": next_month_list,
            "starting_weekday": starting_weekday,
            "current_year": datetime.now().year,
        }
        return calendar_data
