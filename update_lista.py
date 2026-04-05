from playwright.sync_api import sync_playwright

PAGE_URL = "https://www.cablevisionhd.com/rcn-en-vivo.html"
REFERER = "https://www.cablevisionhd.com/"
ORIGIN = "https://www.cablevisionhd.com"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        )

        stream_url = None

        def handle_response(response):
            nonlocal stream_url
            url = response.url

            if ".m3u8" in url:
                stream_url = url
                print("Stream capturado:", stream_url)

        page.on("response", handle_response)

        print("Abriendo página...")
        page.goto(PAGE_URL, wait_until="domcontentloaded", timeout=90000)

        page.wait_for_timeout(15000)

        browser.close()

        if stream_url:
            m3u = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer={REFERER}
#EXTVLCOPT:http-origin={ORIGIN}
{stream_url}
"""

            with open("lista.m3u", "w", encoding="utf-8") as f:
                f.write(m3u)

            print("Lista IPTV actualizada correctamente")
        else:
            raise Exception("No se encontró ningún stream .m3u8")


if __name__ == "__main__":
    run()
