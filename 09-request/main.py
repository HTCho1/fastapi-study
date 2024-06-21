from fastapi import FastAPI, Query


app = FastAPI()


@app.get("/users/")
def read_user(q: str = Query(None, max_length=50)):
    return {"q": q}


# 파라미터 이름을 alias로 명시
@app.get("/items/")
def read_items(internal_query: str = Query(None, alias="search")):
    return {"query_handled": internal_query}


# deprecated=True: 사용자에게 해당 파라미터를 향후 사용하지 말 것을 권장
# 추후에 업데이트를 통해 q라는 파라미터가 사라짐
@app.get("/tools/")
def read_tools(q: str = Query(None, deprecated=True)):
    return {'q': q}


# 해당 파라미터에 대한 설명 -> 지동 문서화
@app.get("/info/")
def read_info(info: str = Query(None, description="정보를 입력하세요.")):
    return {"info": info}


@app.get("/equips/")
def read_equips(
    string_query: str = Query(default="default value", min_length=2, max_length=5, regex="^[a-zA-Z]+$", title="String Query", example="abc"),
    number_query: float = Query(default=1.0, ge=0.5, le1=10.5, title="Number Query", example=5.5)
):
    return {
        "string_query_handled": string_query,
        "number_query_handled": number_query
    }
    