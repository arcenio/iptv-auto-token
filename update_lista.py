import re
from playwright.sync_api import sync_playwright

url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url, timeout=60000)

    html = page.content()

    patron = r'https?://[^"\']+\.m3u8[^"\']*'
    encontrados = re.findall(patron, html)

    if encontrados:

        enlace = encontrados[0]

        lista = "#EXTM3U\n"
        lista += "#EXTINF:-1,RCN En Vivo\n"
        lista += enlace + "\n"

        with open("lista.m3u","w",encoding="utf-8") as f:
            f.write(lista)

        print("M3U8 encontrado:", enlace)

    else:
        print("No se encontró enlace m3u8")

    browser.close()
