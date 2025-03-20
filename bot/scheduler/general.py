from functools import partial
from typing import Any, Callable, Optional

from apscheduler import AsyncScheduler, ConflictPolicy, RunState, Schedule, Task
from apscheduler.abc import DataStore, Trigger

from bot.utils.logger import scheduler_logger


class CustomScheduler(AsyncScheduler):
    """
    Wrapper for apscheduler.

    This class provides some additional features:
        - Custom logging.
        - Configuring and adding schedules in one function.
        - Wrapping functions in partial + args/kwargs by default.
        - Returned schedule after it is added.

    Usage:
        scheduler = CustomScheduler(data_store=SQLAlchemyDataStore(engine_or_url=engine))
        run_date = datetime.now() + timedelta(seconds=5)
        await scheduler.configure_and_add("test", func=lambda: print("Test scheduler"), trigger=run_date)

    Also see:
        - CustomIntervalTrigger (src.scheduler.triggers)
        - CustomCalendarIntervalTrigger (src.scheduler.triggers)
    """

    def __init__(self, data_store: DataStore, enable_logging: bool = False) -> None:
        super().__init__()
        self.enable_logging = enable_logging
        self.data_store = data_store

    def log(self, msg: object, *args: object) -> None:
        if self.enable_logging:
            scheduler_logger.info(msg, *args)

    async def start_in_background(self) -> None:
        self._check_initialized()
        await self._services_task_group.start(self.run_until_stopped)

        if self._state == RunState.started:
            self.log("Scheduler started in background")

    async def cleanup(self) -> None:
        await self.data_store.cleanup()
        self.log("Cleaned up expired job results and finished schedules")

    async def configure_and_add(
        self,
        task_id: str,
        func: Callable,
        trigger: Trigger,
        max_running_jobs: Optional[int] = 1,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[Task, Schedule]:
        task: Task = await self.configure(task_id=task_id, func=func, *args, **kwargs)
        schedule: Schedule = await self.add(
            trigger=trigger,
            task_id=task_id,
            max_running_jobs=max_running_jobs,
        )

        fields = []
        for field in (
            "id",
            "trigger",
            "paused",
            "coalesce",
            "misfire_grace_time",
        ):
            value = getattr(schedule, field)
            if value is not None:
                fields.append(f"{field}={value}")

        self.log(
            "Configured and added new schedule. Schedule(%s)",
            ", ".join(fields),
        )
        return task, schedule

    async def get(self, id: str) -> Schedule:
        return await self.get_schedule(id=id)

    async def configure(
        self, task_id: str, func: Callable, *args: Any, **kwargs: Any
    ) -> Task:
        return await self.configure_task(
            func_or_task_id=task_id, func=partial(func, *args, **kwargs)
        )

    async def add(
        self,
        trigger: Trigger,
        task_id: str,
        max_running_jobs: Optional[int] = 1,
    ) -> Schedule:
        schedule_id: str = await self.add_schedule(
            func_or_task_id=task_id,
            id=task_id,
            trigger=trigger,
            conflict_policy=ConflictPolicy.replace,
            max_running_jobs=max_running_jobs,
        )

        return await self.get(id=schedule_id)
