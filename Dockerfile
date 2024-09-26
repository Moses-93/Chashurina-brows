FROM python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN apt-get install -y wget

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /usr/local/bin/wait-for-it && \
    chmod +x /usr/local/bin/wait-for-it

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "website_browist.wsgi", "python", "manage.py", "migrate"]
