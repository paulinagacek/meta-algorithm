from slither_analysis import analyse_slither
from fastapi import FastAPI
import sys, uvicorn, os

from fastapi.staticfiles import StaticFiles
from routes import router

app = FastAPI()
app.include_router(router)
parent_dir_path = os.path.dirname(os.path.realpath(__file__))
app.mount("/static", StaticFiles(directory=parent_dir_path+"/static"), name="static")

if __name__ == '__main__':
    file_name= r'./example_contracts/lock.sol' # default file
    if len(sys.argv) > 1:
        file_name=sys.argv[1]
    analyse_slither(file_name)
    uvicorn.run("main:app", reload=True)