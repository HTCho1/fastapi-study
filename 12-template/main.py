from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates", auto_reload=True) # auto_reload=True: 템플릿이 변경되면 자동으로 다시 로드


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "username": "Terry Choi", "framework": "FastAPI"}
    ) # 반드시 "request"를 포함해야 함
