from playwright.sync_api import sync_playwright

canales = {
    "RCN": "https://www.cablevisionhd.com/rcn-en-vivo.html",
    "CARACOL": "https://www.cablevisionhd.com/caracol-en-vivo.html",
    "CANAL UNO": "https://www.cablevisionhd.com/canal-uno-en-vivo.html",
}

streams = {}


def capturar_stream(nombre, url):

    stream_url = None

    def capturar_response(response):
        nonlocal stream_url

        link = response.url

        if ".m3u8" in link and "token=" in link:

            stream_url = link

            print(f"Stream encontrado para {nombre}:")
            print(link)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent="Mozilla/5.0"
        )

        page = context.new_page()

        page.on("response", capturar_response)

        print(f"Abriendo {nombre}...")

        page.goto(url)

        page.wait_for_timeout(10000)

        browser.close()

    return stream_url


def generar_lista(streams):

    contenido = "#EXTM3U\n\n"

    for nombre, url in streams.items():

        contenido += f"#EXTINF:-1,{nombre}\n{url}\n\n"

    with open("lista.m3u", "w", encoding="utf-8") as f:

        f.write(contenido)


def main():

    for nombre, url in canales.items():

        stream = capturar_stream(nombre, url)

        if stream:

            streams[nombre] = stream

    if streams:

        generar_lista(streams)

        print("Lista IPTV actualizada")

    else:

        print("No se encontraron streams")


if __name__ == "__main__":
    main()
