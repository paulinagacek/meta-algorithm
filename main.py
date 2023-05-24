from slither_analysis import analyse_slither
from fastapi import FastAPI
import sys, uvicorn

from fastapi.staticfiles import StaticFiles
from routes import router

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    file_name= r'./example_contracts/lock.sol' # default file
    if len(sys.argv) > 1:
        file_name=sys.argv[1]
    analyse_slither(file_name)
    uvicorn.run("main:app", reload=True)