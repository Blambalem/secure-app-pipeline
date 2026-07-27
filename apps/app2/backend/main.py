from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Image Service")

@app.get("/", response_class=HTMLResponse)
def get_image_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Image Service</title>
            <style>
                body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding-top: 50px; }
                img { max-width: 80%; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
            </style>
        </head>
        <body>
            <h1>Привет из второго API! 🖼️</h1>
            <p>Это сервис отдачи изображений и галереи.</p>
            <img src="https://picsum.photos/800/400" alt="Random Image">
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "image-api"}