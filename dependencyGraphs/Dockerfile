FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi","run","graphAPI.py","--port","80"]

#docker run -d --name container -p 80:80 backend