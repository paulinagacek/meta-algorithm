from generate_templates import generate_templates, get_navbar
from fastapi import FastAPI, Request
import sys, uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import router

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        generate_templates(file_name=sys.argv[1])
    else:
        generate_templates()
    uvicorn.run("main:app", reload=True)