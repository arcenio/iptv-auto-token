from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        stream_url = None

        def handle_request(request):
            nonlocal stream_url
            url = request.url

            if ".m3u8" in url:
                stream_url = url
                print("Stream capturado:", stream_url)

        # Escuchar tráfico de red
        page.on("request", handle_request)

        # Abrir página
        page.goto("https://www.cablevisionhd.com/rcn-en-vivo.html", timeout=60000)

        # Esperar a que cargue el player
        page.wait_for_timeout(10000)

        browser.close()

        if stream_url:
            m3u = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://www.cablevisionhd.com/
#EXTVLCOPT:http-origin=https://www.cablevisionhd.com
{stream_url}
"""

            with open("lista.m3u", "w") as f:
                f.write(m3u)

            print("Lista IPTV actualizada correctamente")

        else:
            print("No se encontró ningún stream")

if __name__ == "__main__":
    run()
