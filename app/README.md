## Set up
You can use our app via docker or as a normal python app (if you have masochistic tendecies).
Below you will find some guidence how to set up your environment for both paths.

### Docker (recommended) :whale:
1. You need to have docker installed on your PC
2. Build docker image:
   ```
   docker build -t meta-alg .
   ```
3. Run container
    ```
    docker run -p 80:80 meta-alg
    ```

### Without docker
1. Requirements
- python 3.8+, reccomended 3.8.10
- Linux/ WSL
- gcc

2. Setup Linux/ WSL Ubuntu 20
```bash
    sudo apt-get install python3.x-dev python3.x-venv -y # where x is python version
    sudo apt-get install build-essential python3-dev python3-pip python3-venv python3-wheel -y
```

3. Create virtual env and download all packages
```bash
    python3 -m venv .venv
    source .venv/bin/activate

    pip install numpy
    pip install -r ./requirements.txt
    pip uninstall protobuf
    pip install protobuf==3.20
```

4. Install solc compiler and set version
```bash
    solc-select install 0.8.19
    solc-select use 0.8.19
```

5. Run
```bash
    source .venv/bin/activate
    python app/slither_analysis.py 
    uvicorn app.main:app
```

## Documentation

To see API documentation run application and visit: `http://127.0.0.1:8000/docs`.

## Resources
1. How to Hack Smart Contracts With Slither & Echinda [link](https://www.youtube.com/watch?v=fln_HPA2uOM&t=1473s)