from playwright.sync_api import sync_playwright

sites = [
    "https://www.cablevisionhd.com",
    "https://television-libre.net"
]

streams = {}

def encontrar_paginas(page, base):

    links = page.query_selector_all("a")

    paginas = []

    for link in links:

        href = link.get_attribute("href")

        if href and ("en-vivo" in href or "tv" in href):

            if href.startswith("http"):

                paginas.append(href)

            else:

                paginas.append(base + href)

    return paginas


def capturar_stream(page):

    stream = None

    def detectar(response):

        nonlocal stream

        url = response.url

        if ".m3u8" in url:

            if not stream:

                stream = url

                print("Stream encontrado:", url)

    page.on("response", detectar)

    page.wait_for_timeout(8000)

    return stream


def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context()

        page = context.new_page()

        for site in sites:

            print("Escaneando:", site)

            page.goto(site)

            paginas = encontrar_paginas(page, site)

            print("Paginas encontradas:", len(paginas))

            for url in paginas:

                print("Abriendo:", url)

                page.goto(url)

                stream = capturar_stream(page)

                if stream:

                    nombre = url.split("/")[-1]

                    streams[nombre] = stream

        browser.close()

    contenido = "#EXTM3U\n\n"

    for nombre, url in streams.items():

        contenido += f"#EXTINF:-1,{nombre}\n{url}\n\n"

    with open("lista.m3u", "w", encoding="utf-8") as f:

        f.write(contenido)

    print("Lista IPTV generada")


if __name__ == "__main__":
    main()
