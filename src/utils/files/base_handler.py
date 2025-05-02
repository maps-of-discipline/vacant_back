from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile

from src.logger import get_logger
from src.schemas.document import DocumentSchema
from src.enums import DocumnetTypeEnum

logger = get_logger(__name__)


class BaseFileHandler(ABC):
    """Abstract base class for file handling operations."""

    @abstractmethod
    def get_file_path(
        self, application_id: int, type_: DocumnetTypeEnum, filename: str
    ) -> str:
        """
        Generate a file path based on application ID, document type, and filename.

        Args:
            application_id: ID of the application
            type_: Document type
            filename: Name of the file

        Returns:
            str: Generated file path
        """
        pass

    @abstractmethod
    async def save(self, document: DocumentSchema, file_content: bytes) -> str:
        """
        Save file content to storage and return the file path.

        Args:
            document: Document schema containing metadata
            file_content: The binary content of the file to save

        Returns:
            str: Path where the file was saved
        """
        pass

    @abstractmethod
    async def delete(self, document: DocumentSchema) -> bool:
        """
        Delete a file from storage.

        Args:
            document: Document schema containing filepath to delete

        Returns:
            bool: True if deletion was successful, False otherwise
        """
        pass

    @abstractmethod
    async def get(self, document: DocumentSchema) -> Optional[bytes]:
        """
        Retrieve a file from storage.

        Args:
            document: Document schema containing filepath to retrieve

        Returns:
            Optional[bytes]: File content if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete_by_application_id(self, application_id: int) -> None:
        pass
