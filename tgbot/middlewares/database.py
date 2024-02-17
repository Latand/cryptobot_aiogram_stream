from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update

from infrastructure.database.repo.requests import RequestsRepo


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            event_from_user = data.get("event_from_user")

            user = await repo.users.get_or_create_user(
                user_id=event_from_user.id,
                full_name=event_from_user.full_name,
                language=event_from_user.language_code,
                username=event_from_user.username,
            )
            data["repo"] = repo

            result = await handler(event, data)
        return result
