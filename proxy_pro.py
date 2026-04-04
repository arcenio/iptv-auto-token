from flask import Flask, Response, request
import requests
from seleniumwire import webdriver

app = Flask(__name__)

# Cabeceras que capturaste del streaming original
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Referer": "https://www.cablevisionhd.com/",
    "Origin": "https://www.cablevisionhd.com"
}

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

    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return Response("Error al cargar playlist", status=502, mimetype="text/plain")

    # Reescribir las URLs de segmentos para que pasen por el proxy
    playlist = []
    base_url = url.rsplit("/", 1)[0]
    for line in r.text.splitlines():
        if line.endswith(".ts"):
            # Redirigir segmentos al proxy
            proxied = f"/segment?src={base_url}/{line}"
            playlist.append(proxied)
        else:
            playlist.append(line)

    return Response("\n".join(playlist), mimetype="application/vnd.apple.mpegurl")

@app.route("/segment")
def segment():
    src = request.args.get("src")
    if not src:
        return Response("Segmento no especificado", status=400)

    r = requests.get(src, headers=HEADERS, stream=True)
    if r.status_code == 200:
        return Response(r.content, mimetype="video/mp2t")
    else:
        return Response("Error al cargar segmento", status=502)
