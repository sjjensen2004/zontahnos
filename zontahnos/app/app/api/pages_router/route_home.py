from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
home_router = APIRouter()

@home_router.get("/", include_in_schema=False)
async def home(request: Request):
	return templates.TemplateResponse("pages/home.html",{"request":request})