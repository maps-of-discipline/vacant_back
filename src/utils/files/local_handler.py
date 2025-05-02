import os
import shutil
from typing import Optional
from pathlib import Path
from uuid import uuid4

from src.logger import get_logger
from src.settings import settings
from .base_handler import BaseFileHandler
from src.schemas.document import DocumentSchema
from src.enums import DocumnetTypeEnum

logger = get_logger(__name__)


class LocalFileHandler(BaseFileHandler):
    def __init__(self):
        self.base_dir = Path(settings.file_storage.base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"LocalFileHandler initialized: {self.base_dir}")

    def get_file_path(
        self, application_id: int, type_: DocumnetTypeEnum, filename: str
    ) -> str:
        return f"applications/{application_id}/{type_.value}/{filename}"

    async def save(self, document: DocumentSchema, file_content: bytes) -> str:
        full_path = self.base_dir / document.filepath
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        try:
            with open(full_path, "wb") as f:
                f.write(file_content)
            return document.filepath
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise

    async def delete(self, document: DocumentSchema) -> bool:
        if not document.filepath:
            return False

        full_path = self.base_dir / document.filepath

        if not os.path.exists(full_path):
            return False

        try:
            os.remove(full_path)
            return True
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False

    async def get(self, document: DocumentSchema) -> Optional[bytes]:
        if not document.filepath:
            return None

        full_path = self.base_dir / document.filepath

        if not os.path.exists(full_path):
            return None

        try:
            with open(full_path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to retrieve file: {e}")
            return None

    async def delete_by_application_id(self, application_id: int) -> None:
        fullpath = self.base_dir / f"applications/{application_id}"
        shutil.rmtree(fullpath)
