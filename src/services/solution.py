from io import BytesIO

from fastapi import Depends
from pydantic import BaseModel

from src.documents.solution import SolutionRenderer
from src.exceptions.http import EntityNotFoundHTTPException
from src.gateways.maps import MapsAPIGateway
from src.repository.applications.application import ApplicationRepository
from src.repository.program import ProgramRepository
from src.repository.user import UserRepository
from src.schemas.rups import GetRupDataSchema
from src.services.rups import RupService
from src.models import Program
from src.schemas.solution import GetSolutionRequestSchema


class SolutionService:
    def __init__(
        self,
        renderer: SolutionRenderer = Depends(),
        application_repo: ApplicationRepository = Depends(),
        maps_gateway: MapsAPIGateway = Depends(),
        rup_service: RupService = Depends(),
        user_repo: UserRepository = Depends(),
        program_repo: ProgramRepository = Depends(),
    ):
        self._renderer = renderer
        self._application_repo = application_repo
        self._maps_gateway = maps_gateway
        self._rup_service = rup_service
        self._user_repo = user_repo
        self._program_repo = program_repo

    async def get_solution(self, data: GetSolutionRequestSchema) -> tuple[BytesIO, str]:
        application = await self._application_repo.get_raw(data.application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        user = await self._user_repo.get(application.user_id)
        if not user:
            raise EntityNotFoundHTTPException("User")

        programs = await self._program_repo.get_by_application_id(application.id)
        source: Program = list(filter(lambda el: el.type == "current", programs))[0]
        target: Program = list(
            filter(lambda el: el.type == data.program_type, programs)
        )[0]

        rup_data = await self._rup_service.get_rup_data(
            GetRupDataSchema.model_validate(
                {
                    "source": {
                        "num": source.profile,
                        "sem": source.sem_num,
                    },
                    "target": {
                        "num": target.profile,
                        "sem": target.sem_num,
                    },
                }
            )
        )

        aup_info = await self._maps_gateway.get_aup_info(target.profile)

        file = self._renderer.solution(
            user=user,
            application_type=application.type,
            rup_data=rup_data,
            aup_num=target.profile,
            aup_info=aup_info,
            target=target,
        )

        filename = f"{user.shotname} решение по ЗВМ.docx"

        return file, filename
