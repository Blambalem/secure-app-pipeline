FROM python:3.12-alpine

# Update system packages
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

WORKDIR /app

COPY backend/requirements.txt .

# Upgrade pip, setuptools, wheel AND install project requirements in a single step
RUN pip install --no-cache-dir --upgrade pip wheel "setuptools>=78.1.1" "msgpack>=1.2.1" && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]