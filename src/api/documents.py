import urllib.parse
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse

from src.schemas.user import UserSchema
from src.services.documents import DocumentService
from src.services.auth import PermissionRequire as Require
from src.enums import PermissionsEnum as p


router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/reinstatement/{application_id}")
async def generate_reinstatement_document(
    application_id: int,
    document_service: DocumentService = Depends(),
    user: UserSchema = Depends(Require([])),
):
    """
    Generate a reinstatement application PDF document for a user.

    Args:
        user_id: ID of the user for whom to generate the document

    Returns:
        PDF document as a streaming response
    """

    pdf_content = await document_service.generate_reinstatement_document(
        user, application_id
    )

    encoded_filename = urllib.parse.quote(f"{user.shotname} Заявление на перевод.pdf")
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"

    return Response(
        content=pdf_content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": content_disposition},
    )
