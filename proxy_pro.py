from flask import Flask, Response
from playwright.sync_api import sync_playwright
import requests
import time
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

LAST_STREAM = None
LAST_UPDATE = 0


def get_stream():
    global LAST_STREAM, LAST_UPDATE

    # Cache por 5 minutos
    if time.time() - LAST_UPDATE < 300 and LAST_STREAM:
        return LAST_STREAM

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()

        stream_url = None

        def handle_request(request):
            nonlocal stream_url
            if ".m3u8" in request.url:
                stream_url = request.url

        page.on("request", handle_request)

        try:
            page.goto("https://www.cablevisionhd.com/rcn-en-vivo.html", timeout=60000)
            # Espera hasta que aparezca un request con .m3u8 o máximo 30s
            page.wait_for_response(lambda r: ".m3u8" in r.url, timeout=30000)
        except Exception as e:
            logging.error("Error cargando página: %s", e)

        browser.close()

        if stream_url:
            LAST_STREAM = stream_url
            LAST_UPDATE = time.time()
            logging.info("Nuevo stream: %s", stream_url)

        return LAST_STREAM


@app.route("/")
def home():
    return "IPTV Proxy funcionando 🚀"


@app.route("/rcn.m3u8")
def proxy():
    stream = get_stream()

    if not stream:
        return "Error obteniendo stream", 500

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.cablevisionhd.com/",
        "Origin": "https://www.cablevisionhd.com"
    }

    try:
        r = requests.get(stream, headers=headers, stream=True)
        return Response(
            r.iter_content(chunk_size=1024),
            content_type=r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
        )
    except Exception as e:
        logging.error("Error en proxy: %s", e)
        return f"Error en proxy: {str(e)}", 500


# Nota: no usamos app.run() aquí porque Railway levantará Gunicorn con el Procfile
