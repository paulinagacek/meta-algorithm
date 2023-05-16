from generate_templates import generate_templates, get_navbar
from fastapi import FastAPI, Request
import sys, uvicorn
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="html")

@app.get("/", response_class=HTMLResponse)
async def home_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "nav_bar": get_navbar('Home')})

@app.get("/warnings", response_class=HTMLResponse)
async def warnings_get(request: Request):
    return templates.TemplateResponse("warnings.html", {"request": request, "nav_bar": get_navbar('Warnings')})

@app.get("/vulnerabilities", response_class=HTMLResponse)
async def vulnerabilities_get(request: Request):
    return templates.TemplateResponse("vulnerabilities.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})

@app.get("/symbolic-exec", response_class=HTMLResponse)
async def symbolic_exec_get(request: Request):
    return templates.TemplateResponse("symbolic_execution.html", {"request": request, "nav_bar": get_navbar('Vulnerabilities')})

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_templates(file_name=sys.argv[1])
    else:
        generate_templates()
    uvicorn.run("main:app", reload=True)