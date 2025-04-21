from fastapi import Depends
from src.repository.common_messges import MessagesRepository
from src.repository.status import StatusRepository
from src.schemas.status import StatusGetListSchema


class StatusService:
    def __init__(
        self,
        status_repo: StatusRepository = Depends(),
        messages_repo: MessagesRepository = Depends(),
    ):
        self._status_repo = status_repo
        self._messages_repo = messages_repo

    async def get_all(self) -> list[StatusGetListSchema]:
        res = list()
        statuses = await self._status_repo.get_all()
        for status in statuses:
            messages = await self._messages_repo.get_by_status_id(status.id)
            res.append(
                StatusGetListSchema(
                    title=status.title,
                    verbose_name=status.verbose_name,
                    messages=[el.title for el in messages],
                )
            )

        return res
