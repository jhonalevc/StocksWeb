FROM python:3

RUN apt-get update

WORKDIR /app

COPY . .

EXPOSE 8080

RUN pip install -r requirements.txt

CMD ["python", "stocksweb.py" ]

