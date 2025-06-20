import urllib.parse
from typing import Literal

from fastapi import APIRouter, Depends, Response

from src.schemas.solution import GetSolutionRequestSchema
from src.schemas.document import GetTransferCertificateSchemaRequest
from src.schemas.user import UserSchema
from src.services.auth import PermissionRequire as Require
from src.services.documents import DocumentService
from src.services.solution import SolutionService
from src.services.transfer_certificate import TransferCertificateService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/transfer/{application_id}")
async def generate_transfer_document(
    application_id: int,
    user: UserSchema = Depends(Require([])),
    document_service: DocumentService = Depends(),
):
    pdf_content = await document_service.generate_transfer_document(
        user, application_id
    )

    encoded_filename = urllib.parse.quote(f"{user.shotname} Заявление на перевод.pdf")
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
    pdf_bytes = pdf_content.getvalue()

    headers = {
        "Content-Disposition": content_disposition, 
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )

@router.get("/reinstatement/{application_id}")
async def generate_reinstatement_document(
    application_id: int,
    user: UserSchema = Depends(Require([])),
    document_service: DocumentService = Depends(),
):
    pdf_content = await document_service.generate_reinstatement_document(
        user, application_id
    )
    encoded_filename = urllib.parse.quote(f"{user.shotname} Заявление на восстановление.pdf")
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
    pdf_bytes = pdf_content.getvalue()
    
    headers = {
        "Content-Disposition": content_disposition, 
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )

@router.get("/change/{application_id}")
async def generate_change_document(
    application_id: int,
    user: UserSchema = Depends(Require([])),
    document_service: DocumentService = Depends(),
):
    pdf_content = await document_service.generate_change_document(
        user, application_id
    )

    encoded_filename = urllib.parse.quote(f"{user.shotname} Заявление на изменение условий обучения.pdf")
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
    pdf_bytes = pdf_content.getvalue()
    
    headers = {
        "Content-Disposition": content_disposition, 
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )


@router.get("/solution")
async def generate_solution_document(
    data: GetSolutionRequestSchema = Depends(),
    service: SolutionService = Depends(),
):
    file, filename = await service.get_solution(data)

    encoded_filename = urllib.parse.quote(filename)
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
    pdf_bytes = file.getvalue()

    headers = {
        "Content-Disposition": content_disposition,
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )


@router.get("/transfer-certificate")
async def generate_transfer_certificate(
    data: GetTransferCertificateSchemaRequest = Depends(),
    service: TransferCertificateService = Depends(),
):
    file, filename = await service.render(data.application_id, data.program_type)

    encoded_filename = urllib.parse.quote(filename)
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"
    pdf_bytes = file.getvalue()

    headers = {
        "Content-Disposition": content_disposition,
        "Access-Control-Expose-Headers": "Content-Disposition",
    }

    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )
