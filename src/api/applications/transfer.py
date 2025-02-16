from fastapi import APIRouter


router = APIRouter(prefix='/transfer')


@router.get("/hello")
def say_hello():
    return 'Hello world'