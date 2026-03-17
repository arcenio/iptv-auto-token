from playwright.sync_api import sync_playwright

URL = "https://www.cablevisionhd.com/rcn-en-vivo.html"

def main():

    stream = None

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        def detectar(response):

            nonlocal stream

            if ".m3u8" in response.url:

                if not stream:

                    stream = response.url
                    print("Stream encontrado:")
                    print(stream)

        page.on("response", detectar)

        print("Abriendo página...")

        page.goto(URL)

        page.wait_for_timeout(10000)

        browser.close()

    if stream:

        contenido = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://regionales.saohgdasregions.fun/
#EXTVLCOPT:http-origin=https://regionales.saohgdasregions.fun
{stream}
"""

        with open("lista.m3u","w",encoding="utf-8") as f:

            f.write(contenido)

        print("lista.m3u actualizada")

    else:

        print("No se encontró el stream")

if __name__ == "__main__":
    main()
