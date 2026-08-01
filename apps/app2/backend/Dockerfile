FROM python:3.12-alpine

RUN apk update && apk upgrade && \
    pip install --no-cache-dir --upgrade pip wheel "setuptools>=78.1.1" \
      "msgpack>=1.2.1"

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]