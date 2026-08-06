from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Монтируем локальную папку static по URL-пути /static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def get_image_page():
    # ОБРАТИТЕ ВНИМАНИЕ: путь к картинке указываем относительный к сервису!
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

            <!-- Указываем путь к нашему монтированному ресурсу -->
            <img src="static/bibizana.jpg" alt="Мое локальное фото">
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "image-api"}
