from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Cat(BaseModel):
	name: str
		
		
class Dog(BaseModel):
	name: str
		
		
@app.get("/animal/", response_model=Union[Cat, Dog])
async def get_animal(animal: str):
	if animal == "cat":
		return Cat(name="Whiskers")
	else:
		return Dog(name="Fido")
# uvicorn main_union:app --reload