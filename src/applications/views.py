from src.applications import router


@router.get("/hello")
def say_hello():
    return {"msg": "hello world!"}

