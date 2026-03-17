import requests
import re

URL = "https://www.cablevisionhd.com/rcn-en-vivo.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=20)
html = r.text

match = re.search(r"https://[^\"']+\.m3u8[^\"']+", html)

if match:
    stream = match.group(0)

    m3u = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://regionales.saohgdasregions.fun/
#EXTVLCOPT:http-origin=https://regionales.saohgdasregions.fun
{stream}
"""

    with open("lista.m3u", "w") as f:
        f.write(m3u)

    print("Stream actualizado")
else:
    print("No se encontró stream")
