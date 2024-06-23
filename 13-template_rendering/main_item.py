from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/items")
def read_items(request: Request):
    my_items = ["apple", "banana", "cherry"]
    return templates.TemplateResponse(
        "item.html", {"request": request, "items": my_items})
# http://127.0.0.1:8000/items


@app.get("/dynamic_items/")
def dynamic_items(request: Request, item_list: str = ""):
    items = item_list.split(",")
    return templates.TemplateResponse(
        "item.html", {"request": request, "items": items})
# http://127.0.0.1:8000/dynamic_items?item_list=apple,banana,cherry
# uvicorn main_item:app --reload