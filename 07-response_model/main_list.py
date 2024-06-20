from typing import List
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
	name: str
		
		
@app.get("/items/", response_model=List[Item])
async def get_items():
	return [{"name": "Item 1"}, {"name": "Item 2"}]
# uvicorn main_list:app --reload