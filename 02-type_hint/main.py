from fastapi import FastAPI, Query
from typing import List, Dict, Union, Optional


app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/getdata/")
def read_items(data: str = "funcoding"):
    return {"data": data}


@app.get("/dataitems/")
async def read_items(data: Optional[str] = None):
    return data


@app.get("/items/")
async def read_items(q: List[int] = Query([])):
    return {"q": q}


@app.post("/create-item/")
async def create_item(item: Dict[str, int]):
    return item
