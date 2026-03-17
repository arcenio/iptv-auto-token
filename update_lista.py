from playwright.sync_api import sync_playwright

BASE_URL = "https://www.cablevisionhd.com"

streams = {}


def encontrar_canales(page):

    print("Buscando canales...")

    enlaces = page.query_selector_all("a")

    canales = {}

    for e in enlaces:

        href = e.get_attribute("href")

        if href and "-en-vivo" in href:

            nombre = href.replace("-en-vivo.html", "").replace("-", " ").upper()

            url = BASE_URL + "/" + href

            canales[nombre] = url

    return canales


def capturar_stream(page, nombre, url):

    stream_encontrado = None

    def detectar(response):

        nonlocal stream_encontrado

        link = response.url

        if ".m3u8" in link:

            if not stream_encontrado:

                stream_encontrado = link

                print(f"Stream detectado para {nombre}")
                print(link)

    page.on("response", detectar)

    print(f"Abrendo {nombre}")

    page.goto(url)

    page.wait_for_timeout(10000)

    return stream_encontrado


def generar_lista():

    contenido = "#EXTM3U\n\n"

    for nombre, url in streams.items():

        contenido += f"#EXTINF:-1 group-title=\"TV\",{nombre}\n{url}\n\n"

    with open("lista.m3u", "w", encoding="utf-8") as f:

        f.write(contenido)


def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0"
        )

        page = context.new_page()

        print("Abriendo página principal...")

        page.goto(BASE_URL)

        canales = encontrar_canales(page)

        print(f"Canales encontrados: {len(canales)}")

        for nombre, url in canales.items():

            stream = capturar_stream(page, nombre, url)

            if stream:

                streams[nombre] = stream

        browser.close()

    if streams:

        generar_lista()

        print("Lista IPTV creada")

    else:

        print("No se encontraron streams")


if __name__ == "__main__":
    main()
