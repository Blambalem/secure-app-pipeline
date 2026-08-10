FROM python:3.12-alpine

RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

WORKDIR /app

COPY backend/requirements.txt .

# Флаг --upgrade заставит pip обновить уже существующие setuptools и msgpack до версий из requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY backend/ .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]