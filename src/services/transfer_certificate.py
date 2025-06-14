from io import BytesIO

from fastapi import Depends

from src.documents.transfer_certificate import TransferCertificateRenderer
from src.exceptions.http import EntityNotFoundHTTPException
from src.gateways.maps import MapsAPIGateway
from src.repository.applications.application import ApplicationRepository
from src.repository.program import ProgramRepository
from src.repository.user import UserRepository
from src.services.rups import RupService
from src.models import Program


class TransferCertificateService:
    def __init__(
        self,
        renderer: TransferCertificateRenderer = Depends(),
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

    async def render(self, application_id: int, program_type: str) -> tuple[BytesIO, str]:
        application = await self._application_repo.get_raw(application_id)
        if not application:
            raise EntityNotFoundHTTPException("Application")

        user = await self._user_repo.get(application.user_id)
        if not user:
            raise EntityNotFoundHTTPException("User")

        programs = await self._program_repo.get_by_application_id(application_id)
        chosen_program: Program = list(filter(lambda el: el.type == program_type, programs))[0]

        all_maps = await self._maps_gateway.get_all_maps()
        direction = all_maps.get_direction_by_num(chosen_program.profile)

        file = self._renderer.render(
            fullname=user.fullname,
            program=direction.name,
        )

        filename = f"{user.shotname} справка о переводе.docx"
        return file, filename
