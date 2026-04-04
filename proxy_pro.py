from flask import Flask, Response
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

        # Espera unos segundos para que cargue el reproductor
        driver.implicitly_wait(10)

        m3u8_url = None
        for request in driver.requests:
            if request.response and ".m3u8" in request.url:
                m3u8_url = request.url
                break

        driver.quit()

        if m3u8_url:
            print(f"✅ Nuevo stream capturado: {m3u8_url}")
            return m3u8_url
        else:
            print("⚠️ No se encontró ningún enlace .m3u8 en las peticiones de red")
            return None
    except Exception as e:
        print(f"❌ Error en get_stream: {e}")
        return None

@app.route("/")
def home():
    return "Proxy IPTV funcionando 🚀"

@app.route("/rcn.m3u8")
def rcn():
    # Cada vez que VLC pide este endpoint, se regenera el enlace
    url = get_stream()
    if url:
        return Response(f"#EXTM3U\n#EXTINF:-1,RCN\n{url}", mimetype="application/vnd.apple.mpegurl")
    else:
        return Response("Stream no disponible", status=503, mimetype="text/plain")
