
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
   return templates.TemplateResponse('Main1.html', {"request": request})

@app.get("/main")
async def root():
    return {"message": "Hoang Tuan"}       


#uvicorn.run(app, host="0.0.0.0", port=90)

