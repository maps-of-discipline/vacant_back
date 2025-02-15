from fastapi.routing import APIRouter

router = APIRouter(
    prefix='/applications',
)

import src.applications.models
import src.applications.views




