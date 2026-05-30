import logging
from fastapi import FastAPI

# Настраиваем базовое логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Secure App")

@app.get("/")
def read_root():
    return {"message": "Hello, Security World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy, testing"}
