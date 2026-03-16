from playwright.sync_api import sync_playwright

url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

m3u8_encontrado = None

def capturar_respuesta(response):
    global m3u8_encontrado
    if ".m3u8" in response.url:
        m3u8_encontrado = response.url

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("response", capturar_respuesta)

    page.goto(url, timeout=60000)

    page.wait_for_timeout(15000)

    if m3u8_encontrado:

        contenido = "#EXTM3U\n"
        contenido += "#EXTINF:-1 tvg-id=\"rcn\" tvg-name=\"RCN\" group-title=\"TV\",RCN En Vivo\n"
        contenido += "#EXTVLCOPT:http-referrer=https://www.cablevisionhd.com/\n"
        contenido += "#EXTVLCOPT:http-user-agent=Mozilla/5.0\n"
        contenido += m3u8_encontrado + "\n"

        with open("lista.m3u","w",encoding="utf-8") as f:
            f.write(contenido)

        print("M3U8 capturado:", m3u8_encontrado)

    else:
        print("No se detecto ningun m3u8")

    browser.close()
