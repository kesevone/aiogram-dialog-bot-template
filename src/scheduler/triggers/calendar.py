from datetime import time, timedelta

import attrs
from apscheduler.triggers.calendarinterval import CalendarIntervalTrigger


@attrs.define(kw_only=True)
class CustomCalendarIntervalTrigger(CalendarIntervalTrigger):
    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    hour: int = 0
    minute: int = 0
    second: int = 0
    start_by_trigger: bool = True

    def __attrs_post_init__(self) -> None:
        self._time = time(self.hour, self.minute, self.second, tzinfo=self.timezone)

        if self.years == self.months == self.weeks == self.days == 0:
            raise ValueError("interval must be at least 1 day long")

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("end_date cannot be earlier than start_date")

        # Add the interval from the trigger to the current date, because we don't want to run the task when the script is running.
        if self.start_by_trigger:
            self.start_date += timedelta(days=self.days, weeks=self.weeks)