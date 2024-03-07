from aiogram_dialog import DialogManager


async def get_user_data(dialog_manager: DialogManager, **_kwargs):
    """
    Get user data from an aiogram event.
    """
    user = dialog_manager.event.from_user
    return {
        'user_id': user.id,
        'username': user.username,
        'full_name': user.full_name,
    }