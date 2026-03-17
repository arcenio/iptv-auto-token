from playwright.sync_api import sync_playwright

url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

m3u8_lista = []

def capturar_respuesta(response):
    global m3u8_lista
    enlace = response.url

    if ".m3u8" in enlace:
        m3u8_lista.append(enlace)

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("response", capturar_respuesta)

    page.goto(url, timeout=60000)

    page.wait_for_timeout(20000)

    if m3u8_lista:

        enlace_final = m3u8_lista[-1]

        contenido = "#EXTM3U\n"
        contenido += "#EXTINF:-1 tvg-id=\"rcn\" tvg-name=\"RCN\" group-title=\"TV\",RCN En Vivo\n"
        contenido += "#EXTVLCOPT:http-referrer=https://regionales.saohgdasregions.fun/\n"
        contenido += "#EXTVLCOPT:http-origin=https://regionales.saohgdasregions.fun\n"
        contenido += "#EXTVLCOPT:http-user-agent=Mozilla/5.0\n"
        contenido += enlace_final + "\n"

        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(contenido)

        print("M3U8 usado:", enlace_final)

    else:
        print("No se detecto m3u8")

    browser.close()
