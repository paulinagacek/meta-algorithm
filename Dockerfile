FROM python:3.8.10

WORKDIR /code

COPY ./req.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt
RUN solc-select install 0.8.19
RUN solc-select use 0.8.19

COPY ./app /code/app
COPY ./example_contracts /code/example_contracts

RUN python /code/app/slither_analysis.py

# COPY ./app /code/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]