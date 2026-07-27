FROM python:3.12-alpine

RUN apk update && apk upgrade && \
    pip install --no-cache-dir --upgrade pip wheel setuptools

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]