from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates", auto_reload=True)


# 경로 파라미터 사용
@app.get("/user/{username}/framework/{framework}")
def read_user(request: Request, username: str, framework: str):
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username, "framework": framework}
    )
# 127.0.0.1:8000/user/terry/framework/FastAPI


# 쿼리 파라미터 사용
@app.get("/user")
def get_user(request: Request, username: str, framework: str):
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": username, "framework": framework}
    )
# 127.0.0.1:8000/user?username=terry&framework=FastAPI


@app.get("/greet")
def greeting(request: Request, time_of_day: str):
    return templates.TemplateResponse(
        "index.html", {"request": request, "time_of_day": time_of_day}
        )
