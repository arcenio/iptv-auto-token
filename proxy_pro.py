from flask import Flask, Response
import requests
from seleniumwire import webdriver

app = Flask(__name__)

def get_stream():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.cablevisionhd.com/rcn-en-vivo.html")
        driver.implicitly_wait(10)

        m3u8_url = None
        for req in driver.requests:
            if req.response and ".m3u8" in req.url:
                m3u8_url = req.url
                break

        driver.quit()
        return m3u8_url
    except Exception as e:
        print(f"❌ Error en get_stream: {e}")
        return None

@app.route("/")
def home():
    return "Proxy IPTV funcionando 🚀"

@app.route("/rcn.m3u8")
def rcn():
    url = get_stream()
    if not url:
        return Response("Stream no disponible", status=503, mimetype="text/plain")

    # Pedimos el .m3u8 real con cabeceras necesarias
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.cablevisionhd.com/",
        "Origin": "https://www.cablevisionhd.com"
    }
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return Response(r.text, mimetype="application/vnd.apple.mpegurl")
    else:
        return Response("Error al cargar stream", status=502, mimetype="text/plain")
