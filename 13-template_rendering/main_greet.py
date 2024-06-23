from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates", auto_reload=True)


@app.get("/greet")
def greeting(request: Request, time_of_day: str):
    return templates.TemplateResponse(
        "index_greet.html", {"request": request, "time_of_day": time_of_day}
    )
# uvicorn main_greet:app --reload