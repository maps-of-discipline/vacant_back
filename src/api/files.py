from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi.responses import Response
from src.logger import get_logger
from src.services.file import FileService
from src.exceptions.http import EntityNotFoundHTTPException
import urllib.parse

logger = get_logger(__name__)

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{document_id}")
async def get_file(
    document_id: int = Path(..., description="Document ID"),
    file_service: FileService = Depends(),
) -> Response:
    logger.info(f"Start handling file download for document ID {document_id}")

    filename, content = await file_service.get_document_file(document_id)

    if not filename or not content:
        logger.warning(f"File content not found for document ID {document_id}")
        raise EntityNotFoundHTTPException("Document")
    logger.info(f"Successfully retrieved file {filename} for document ID {document_id}")

    encoded_filename = urllib.parse.quote(filename)
    content_disposition = f"attachment; filename=\"{encoded_filename}\"; filename*=UTF-8''{encoded_filename}"

    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={"Content-Disposition": content_disposition},
    )

