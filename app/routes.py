from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
import pickle, os
from jinja2 import Environment, FileSystemLoader

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

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
templates = Jinja2Templates(directory=parent_dir_path+"/templates")
temporary = Jinja2Templates(directory=parent_dir_path+"/temp")


@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home')})

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