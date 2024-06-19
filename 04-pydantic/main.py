from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 0.1
    
    
app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return {"item": item.dict()}
