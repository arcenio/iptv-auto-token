import requests
import re

# URL donde REALMENTE está el player
url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    r = requests.get(url, headers=headers, timeout=20)
    html = r.text

    # Buscar iframe (donde está el verdadero reproductor)
    iframe = re.search(r'<iframe[^>]+src="([^"]+)"', html)

    if iframe:
        iframe_url = iframe.group(1)
        print("Iframe encontrado:", iframe_url)

        r2 = requests.get(iframe_url, headers=headers, timeout=20)
        html2 = r2.text

        # Buscar m3u8 dentro del iframe
        stream = re.search(r"https://[^\"']+\.m3u8[^\"']+", html2)

        if stream:
            stream_url = stream.group(0)

            print("Stream encontrado:", stream_url)

            m3u = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://regionales.saohgdasregions.fun/
#EXTVLCOPT:http-origin=https://regionales.saohgdasregions.fun
{stream_url}
"""

            with open("lista.m3u", "w") as f:
                f.write(m3u)

            print("Lista actualizada correctamente")

        else:
            print("No se encontró stream en iframe")

    else:
        print("No se encontró iframe")

except Exception as e:
    print("Error:", e)
