from fastapi import APIRouter


router = APIRouter(prefix='/change')

@router.post("")
def create_change_application(

):
    return 'Hello world'