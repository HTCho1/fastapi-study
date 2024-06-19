from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


# Path Parameters
@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}


# Query Parameters
@app.get("/items/")
def read_items(skip=0, limit=10):
    return {"skip": skip, "limit": limit}
