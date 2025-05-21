FROM python:3.12-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./app .

CMD ["fastmcp", "run", "app.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
