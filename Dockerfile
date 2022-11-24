FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

VOLUME ["/db"]

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
