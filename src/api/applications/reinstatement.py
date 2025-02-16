from fastapi import APIRouter


router = APIRouter(prefix='/reinstatement')


@router.get("/hello")
def say_hello():
    return 'Hello world'