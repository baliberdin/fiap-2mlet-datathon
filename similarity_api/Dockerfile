FROM python:3.13.3-slim

WORKDIR /opt/similarity-api

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./secrets ./secrets
COPY ./main.py ./main.py
COPY ./services ./services
COPY ./configuration ./configuration
COPY ./api ./api

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "80"]