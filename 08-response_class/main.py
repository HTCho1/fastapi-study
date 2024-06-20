from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, PlainTextResponse


app = FastAPI()


@app.get("/json", response_class=JSONResponse)
def read_json():
    return {"msg": "This is JSON"}


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return "<h1>This is HTML</h1>"



@app.get("/text", response_class=PlainTextResponse)
def read_text():
		return "This is Plain Text"


@app.get("/redirect")
def read_redirect():
		return RedirectResponse(url="/text")
