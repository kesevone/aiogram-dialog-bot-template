from datetime import timedelta

import attrs
from apscheduler.triggers.interval import IntervalTrigger


@attrs.define(kw_only=True)
class CustomIntervalTrigger(IntervalTrigger):
    weeks: float = 0
    days: float = 0
    hours: float = 0
    minutes: float = 0
    seconds: float = 0
    microseconds: float = 0
    start_by_trigger: bool = True

    def __attrs_post_init__(self):
        self._interval = timedelta(
            weeks=self.weeks,
            days=self.days,
            hours=self.hours,
            minutes=self.minutes,
            seconds=self.seconds,
            microseconds=self.microseconds,
        )

        if self._interval.total_seconds() <= 0:
            raise ValueError("The time interval must be positive")

        if self.end_time and self.end_time < self.start_time:
            raise ValueError("end_time cannot be earlier than start_time")

        # Add the interval from the trigger to the current date, because we don't want to run the task when the script is running.
        if self.start_by_trigger:
            self.start_time += timedelta(
                weeks=self.weeks,
                days=self.days,
                hours=self.hours,
                minutes=self.minutes,
                seconds=self.seconds,
                microseconds=self.microseconds,
            )