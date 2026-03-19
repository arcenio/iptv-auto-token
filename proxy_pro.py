from flask import Flask, Response
from playwright.sync_api import sync_playwright
import requests
import time
import os

app = Flask(__name__)

LAST_STREAM = None
LAST_UPDATE = 0

def get_stream():
    global LAST_STREAM, LAST_UPDATE

    if time.time() - LAST_UPDATE < 300 and LAST_STREAM:
        return LAST_STREAM

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        stream_url = None

        def handle_request(request):
            nonlocal stream_url
            if ".m3u8" in request.url:
                stream_url = request.url

        page.on("request", handle_request)

        page.goto("https://www.cablevisionhd.com/rcn-en-vivo.html", timeout=60000)
        page.wait_for_timeout(8000)

        browser.close()

        if stream_url:
            LAST_STREAM = stream_url
            LAST_UPDATE = time.time()
            print("Nuevo stream:", stream_url)

        return LAST_STREAM


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

    r = requests.get(stream, headers=headers, stream=True)

    return Response(
        r.iter_content(chunk_size=1024),
        content_type=r.headers.get("Content-Type")
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
