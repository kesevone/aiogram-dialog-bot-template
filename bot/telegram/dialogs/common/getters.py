from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.database import DBUser


async def get_aiogram_user(dialog_manager: DialogManager, **_kwargs):
    """
    Get user data from an aiogram event.
    """
    user: User = dialog_manager.event.from_user
    return {
        "user_id": user.id,
        "username": user.username,
        "full_name": user.full_name,
    }


async def get_db_user(dialog_manager: DialogManager, **_kwargs):
    """
    Get user data from a database.
    """
    db_user: DBUser = dialog_manager.middleware_data["user"]
    return {
        "db_user": db_user,
        "user_id": db_user.id,
        "username": db_user.username,
        "full_name": db_user.full_name,
        "user_is_active": db_user.is_active,
    }
