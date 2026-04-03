from flask import Flask, Response
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def get_stream():
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()

            m3u8_url = None

            # Captura todas las peticiones de red
            def handle_request(request):
                nonlocal m3u8_url
                if ".m3u8" in request.url:
                    m3u8_url = request.url

            page.on("request", handle_request)
            page.goto("https://www.cablevisionhd.com/rcn-en-vivo.html", timeout=60000)
            page.wait_for_timeout(10000)  # espera 10 segundos

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
    url = get_stream()
    if url:
        # devolvemos un playlist simple con el stream real
        return Response(f"#EXTM3U\n#EXTINF:-1,RCN\n{url}", mimetype="application/vnd.apple.mpegurl")
    else:
        return Response("Stream no disponible", status=503, mimetype="text/plain")
