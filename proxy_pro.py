from flask import Flask, Response
import playwright.sync_api as p

app = Flask(__name__)

def get_stream():
    try:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.cablevisionhd.com/rcn-en-vivo.html", timeout=60000)
        page.wait_for_timeout(5000)  # espera 5 segundos

        # buscar enlaces m3u8
        links = page.locator("a[href*='.m3u8']").all()
        if links:
            url = links[0].get_attribute("href")
            print(f"✅ Nuevo stream capturado: {url}")
            return url
        else:
            print("⚠️ No se encontró ningún enlace .m3u8 en la página")
            return None
    except Exception as e:
        print(f"❌ Error en get_stream: {e}")
        return None
    finally:
        browser.close()

@app.route("/")
def home():
    return "Proxy IPTV funcionando 🚀"

@app.route("/rcn.m3u8")
def rcn():
    url = get_stream()
    if url:
        # devolvemos un redirect al stream real
        return Response(f"#EXTM3U\n#EXTINF:-1,RCN\n{url}", mimetype="application/vnd.apple.mpegurl")
    else:
        return Response("Stream no disponible", status=503, mimetype="text/plain")
