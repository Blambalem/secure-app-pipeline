from fastapi import FastAPI

app = FastAPI(title="Secure App")

@app.get("/")
def read_root():
    return {"message": "Hello, Security World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}