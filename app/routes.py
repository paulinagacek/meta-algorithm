from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

import pickle, os
from models import Stats

class NavbarItem:
    def __init__(self, name, endpoint, isSelected, emoji) -> None:
        self.name = name
        self.endpoint = endpoint
        self.isSelected = isSelected
        self.emoji = emoji

nav_bar = [
    NavbarItem('Home', '/', True, "home"),
    NavbarItem('Warnings', '/warnings', False, "warning"),
    NavbarItem('Vulnerabilities', '/vulnerabilities', False, "bug_report"),
    NavbarItem('Symbolic Execution', '/symbolic-exec', False, "bolt"),
    NavbarItem('Info', '/info', False, "info"),
]

def get_navbar(item_name: str):
    for item in nav_bar:
        if item_name == item.name:
            item.isSelected = True
        else:
            item.isSelected = False
    return nav_bar

router = APIRouter()

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=parent_dir_path+"/templates")
temporary = Jinja2Templates(directory=parent_dir_path+"/temp")


@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    with open(parent_dir_path + '/temp/warnings.pickle', 'rb') as handle:
        warnings = pickle.load(handle)
    
    with open(parent_dir_path + '/temp/vulnerabilities.pickle', 'rb') as handle:
        vulnerabilities = pickle.load(handle)
    
    stats = {
        Stats("Warnings", len(warnings)),
        Stats("Vulnerabilities dettected by slither", len(vulnerabilities))
    }
    
    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home'), "stats": stats})

@router.get("/warnings", response_class=HTMLResponse)
async def warnings_get(request: Request):
    with open(parent_dir_path + '/temp/warnings.pickle', 'rb') as handle:
        warnings = pickle.load(handle)
    return templates.TemplateResponse("warnings.html", {"request": request, "nav_bar": get_navbar('Warnings'), "warnings":warnings})

@router.get("/vulnerabilities", response_class=HTMLResponse)
async def vulnerabilities_get(request: Request):
    with open(parent_dir_path + '/temp/vulnerabilities.pickle', 'rb') as handle:
        vulnerabilities = pickle.load(handle)

    # generate html temp file to be able to manipulate DOM in comunicates
    # when trying to render with params it didn't work
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))    
    template_vulnerabilities = env.get_template('vulnerabilities.html')
    des_filename = os.path.join(root, 'temp', 'vulnerabilities.html')

    with open(des_filename, 'w') as fh:
        fh.write(template_vulnerabilities.render(nav_bar=get_navbar('Vulnerabilities'), vulnerabilities=vulnerabilities))
    
    return temporary.TemplateResponse("vulnerabilities.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})

@router.get("/symbolic-exec", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    return templates.TemplateResponse("symbolic_execution.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})

@router.get("/info", response_class=HTMLResponse)
async def info_get(request: Request):
    return templates.TemplateResponse("info.html", {"request": request, "nav_bar": get_navbar('Info')})