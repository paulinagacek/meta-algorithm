# slither

FROM python:3.8.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt
RUN solc-select install 0.8.19
RUN solc-select use 0.8.19

COPY ./app /code/app
COPY ./example_contracts /code/example_contracts

# slither
RUN python /code/app/slither_analysis.py


# echidna
    
RUN apt-get update && \
    apt-get install -y -q --allow-unauthenticated \
    git sudo build-essential curl file

RUN useradd -m -s /bin/bash linuxbrew && \
    usermod -aG sudo linuxbrew &&  \
    mkdir -p /home/linuxbrew/.linuxbrew && \
    chown -R linuxbrew: /home/linuxbrew/.linuxbrew
USER linuxbrew
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"
RUN brew install echidna

WORKDIR /code

USER root
RUN solc-select install 0.8.19
RUN solc-select use 0.8.19
RUN python3 /code/app/echidna_analysis.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]