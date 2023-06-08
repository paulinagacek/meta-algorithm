from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader

import pickle, os, shutil
from os.path import isfile, join
from models import Stats

class NavbarItem:
    def __init__(self, name, endpoint, isSelected: bool, emoji, file_required: bool) -> None:
        self.name = name
        self.endpoint = endpoint
        self.isSelected = isSelected
        self.emoji = emoji
        self.file_required = file_required # if sol file is required to display

nav_bar = [
    NavbarItem('Home', '/', True, "home", False),
    NavbarItem('Warnings', '/warnings', False, "warning", True),
    NavbarItem('Vulnerabilities', '/vulnerabilities', False, "bug_report", True),
    NavbarItem('Symbolic Execution', '/symbolic-exec', False, "bolt", True),
    NavbarItem('Fuzzing', '/fuzzing', False, "quiz", True),
    NavbarItem('Info', '/info', False, "info", False),
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
temp_dir = os.path.join(parent_dir_path, 'temp')
templates = Jinja2Templates(directory=parent_dir_path+"/templates")
temporary = Jinja2Templates(directory=temp_dir)

def get_analysed_filename():
    file_name = ""
    sol_file = [f for f in os.listdir(temp_dir) if isfile(join(temp_dir, f)) and f[-3:]=="sol"]
    if len(sol_file) > 0:
        file_name = sol_file[0]
    return file_name


@router.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    with open(parent_dir_path + '/temp/warnings.pickle', 'rb') as handle:
        warnings = pickle.load(handle)
    
    vur_stats = {"critical": 0, "medium":0, "suggestion": 0}
    with open(parent_dir_path + '/temp/vulnerabilities.pickle', 'rb') as handle:
        vulnerabilities = pickle.load(handle)
        for vur in vulnerabilities:
            vur_stats[vur.impact]+=1
    
    stats = {
        Stats("Warnings", len(warnings)),
        Stats("Vulnerabilities dettected by slither", len(vulnerabilities))
    }

    echidna_stats = {}
    with open(parent_dir_path + '/temp/echidna_stats.pickle', 'rb') as handle:
        echidna_stats = pickle.load(handle)
    
    

    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home'), "stats": stats, "vur_stats": vur_stats, "echidna_stats": echidna_stats, "file_name": get_analysed_filename()})

@router.get("/warnings", response_class=HTMLResponse)
async def warnings_get(request: Request):
    with open(parent_dir_path + '/temp/warnings.pickle', 'rb') as handle:
        warnings = pickle.load(handle)
    return templates.TemplateResponse("warnings.html", {"request": request, "nav_bar": get_navbar('Warnings'), "warnings":warnings, "file_name": get_analysed_filename()})

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
        fh.write(template_vulnerabilities.render(nav_bar=get_navbar('Vulnerabilities'), vulnerabilities=vulnerabilities, file_name=get_analysed_filename()) )
    
    return temporary.TemplateResponse("vulnerabilities.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities'), "file_name": get_analysed_filename()})

@router.get("/symbolic-exec", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    return templates.TemplateResponse("symbolic_execution.html", {"request": request, "nav_bar": get_navbar('Symbolic Execution'), "file_name": get_analysed_filename()})

@router.get("/fuzzing", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    with open(parent_dir_path + '/temp/fuzzing_log.pickle', 'rb') as handle:
        fuzzing_log = pickle.load(handle)
    
    with open(parent_dir_path + '/temp/code_coverage.pickle', 'rb') as handle:
        code_coverage = pickle.load(handle)
    
    with open(parent_dir_path + '/temp/echidna_stats.pickle', 'rb') as handle:
        stats = pickle.load(handle)

    return templates.TemplateResponse("echidna.html", {"request": request, "nav_bar": get_navbar('Fuzzing'), "fuzzing_log": fuzzing_log, "code_coverage": code_coverage,  "echidna_stats": stats, "file_name": get_analysed_filename()})

@router.get("/info", response_class=HTMLResponse)
async def info_get(request: Request):
    return templates.TemplateResponse("info.html", {"request": request, "nav_bar": get_navbar('Info'), "file_name": get_analysed_filename()})

@router.post("/upload", response_class=HTMLResponse)
async def upload(file: UploadFile):
    try:
        filename = file.filename
        if filename.split('.')[-1] != 'sol':
            print("Bad format")
            return RedirectResponse(url='/', status_code=303) # zly format pliku
        
        # clear temp folder
        if os.path.exists(temp_dir):
            # shutil.rmtree(temp_dir)
            sol_file = [f for f in os.listdir(temp_dir) if isfile(join(temp_dir, f)) and f[-3:]=="sol"]
            if len(sol_file) > 0:
                os.remove(join(temp_dir,sol_file[0]))
        # os.mkdir(temp_dir)

        contents = file.file.read()
        with open(os.path.join(temp_dir, file.filename), 'wb') as f:
            f.write(contents)
    except Exception as e:
        print(e)
        return RedirectResponse(url='/', status_code=303) # blad przy zapisywaniu pliku
    finally:
        file.file.close()

    return RedirectResponse(url='/', status_code=303) # wszystko dobrze, proceduj z analiza
