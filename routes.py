from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from generate_templates import generate_templates, get_navbar
from fastapi import FastAPI, Request

router = APIRouter()
templates = Jinja2Templates(directory="html")

@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home')})

@router.get("/warnings", response_class=HTMLResponse)
async def warnings_get(request: Request):
    return templates.TemplateResponse("warnings.html", {"request": request, "nav_bar": get_navbar('Warnings')})

@router.get("/vulnerabilities", response_class=HTMLResponse)
async def vulnerabilities_get(request: Request):
    return templates.TemplateResponse("vulnerabilities.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})

@router.get("/symbolic-exec", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    return templates.TemplateResponse("symbolic_execution.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})