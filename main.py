from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.database import engine
from user import models_user
from user.router_user import router as UserRouter
from auth.authentication import router as AuthenticationRouter
from ai.router_ai import router as AiRouter


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(UserRouter, prefix="/api")
app.include_router(AuthenticationRouter, prefix="/api")
app.include_router(AiRouter, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

models_user.Base.metadata.create_all(bind=engine)