from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
import pickle

class NavbarItem:
    def __init__(self, name, endpoint, isSelected) -> None:
        self.name = name
        self.endpoint = endpoint
        self.isSelected = isSelected

nav_bar = [
    NavbarItem('Home', '/', True),
    NavbarItem('Warnings', '/warnings', False),
    NavbarItem('Vulnerabilities', '/vulnerabilities', False),
    NavbarItem('Symbolic Execution', '/symbolic-exec', False),
]

def get_navbar(item_name: str):
    for item in nav_bar:
        if item_name == item.name:
            item.isSelected = True
        else:
            item.isSelected = False
    return nav_bar

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home')})

@router.get("/warnings", response_class=HTMLResponse)
async def warnings_get(request: Request):
    with open('temp/warnings.pickle', 'rb') as handle:
        warnings = pickle.load(handle)
    return templates.TemplateResponse("warnings.html", {"request": request, "nav_bar": get_navbar('Warnings'), "warnings":warnings})

@router.get("/vulnerabilities", response_class=HTMLResponse)
async def vulnerabilities_get(request: Request):
    with open('temp/vulnerabilities.pickle', 'rb') as handle:
        vulnerabilities = pickle.load(handle)
    return templates.TemplateResponse("vulnerabilities.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities'), "vulnerabilities": vulnerabilities})

@router.get("/symbolic-exec", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    return templates.TemplateResponse("symbolic_execution.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})