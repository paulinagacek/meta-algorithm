## Set up
1. Requirements
- python 3.8+, reccomended 3.8.10
- Linux/ WSL
- gcc

2. Setup Linux/ WSL Ubuntu 20
```bash
    sudo apt-get install python3.x-dev # where x is python version
    sudo apt-get install build-essential 
    sudo apt install python3.x-venv
    sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y
```

3. Create virtual env and dowload all packages
```
python3 -m venv .venv
source .venv/bin/activate

pip install numpy
pip install -r ./requirements.txt
pip uninstall protobuf
pip install protobuf==3.20
```

4. Install solc compiler and set version
```
solc-select install 0.8.19
solc-select use 0.8.19
```

## How to run it

1. Run generate_template.py:
    ```
    source .venv/bin/activate
    python main.py
    ```

## Running with docker :whale:
```
docker run -p 80:80 meta-alg
```

## Documentation

To see API documentation run application and visit: `http://127.0.0.1:8000/docs`.