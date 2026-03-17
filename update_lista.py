import requests
import re

# Página donde está el reproductor
url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    r = requests.get(url, headers=headers, timeout=20)
    html = r.text

    # Buscar cualquier stream m3u8 con token
    match = re.search(r"https://[^\"']+\.m3u8[^\"']+", html)

    if match:
        stream_url = match.group(0)

        print("Stream encontrado:")
        print(stream_url)

        m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="rcn" tvg-name="RCN",RCN
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://regionales.saohgdasregions.fun/
#EXTVLCOPT:http-origin=https://regionales.saohgdasregions.fun
{stream_url}
"""

        with open("lista.m3u", "w") as f:
            f.write(m3u_content)

        print("Lista IPTV actualizada")

    else:
        print("No se encontró ningún stream")

except Exception as e:
    print("Error:", e)
