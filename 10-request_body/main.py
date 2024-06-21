from fastapi import FastAPI, Body


app = FastAPI()


# ...: 해당 파라미터는 필수라는 의미(Required)
@app.post("/items/")
def create_item(item: dict = Body(...)):
    return {"item": item}


# Body는 POST에 사용, GET에는 사용할 수 없음
@app.post("/advanced_items/")
def create_advanced_item(
    item: dict = Body(
        default=None,
        alias="item_alias",
        example={"key": "value"},
        title="Sample Item",
        description="This is a sample item",
        deprecated=False
    ),
    additional_info: dict = Body(
        default=None,
        example={"info_key": "info_value"},
        title="Additional Info",
        description="This is some additional information about the item",
        deprecated=False
    )):
    return {"item": item,
            "additional_info": additional_info}
