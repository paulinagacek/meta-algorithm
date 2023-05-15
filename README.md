## Set up
1. Requirements
- python 3.8+
- Linux/ WSL
- gcc

2. Setup Linux/ WSL
```bash
    sudo apt-get install python3.x-dev # where x is python version
    sudo apt-get install build-essential 
```

3. Create virtual env and dowload all packages
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r ./requirements.txt
```

4. Install solc compiler and set version
```
solc-select install 0.8.19
solc-select use 0.8.19
```

## How to run it

1. Run generate_template.py:
    ```
    .venv\Scripts\activate
    python .\generate_templates.py
    ```