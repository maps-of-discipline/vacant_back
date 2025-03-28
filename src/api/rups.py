from fastapi import APIRouter


router = APIRouter(
    prefix="/rups",
    tags=['rups']
)



@router.get('')
async def get_rups():
    pass
