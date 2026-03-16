import requests
import re

url = "https://www.cablevisionhd.com/rcn-en-vivo.html"

headers = {
"User-Agent": "Mozilla/5.0"
}

try:
    r = requests.get(url, headers=headers, timeout=20)
    html = r.text

    patron = r'https?://[^"\']+\.m3u8[^"\']*'
    encontrados = re.findall(patron, html)

    if encontrados:

        enlace = encontrados[0]

        lista = "#EXTM3U\n"
        lista += "#EXTINF:-1,RCN En Vivo\n"
        lista += enlace + "\n"

        with open("lista.m3u","w",encoding="utf-8") as f:
            f.write(lista)

        print("M3U8 encontrado:")
        print(enlace)

    else:
        print("No se encontro ningun enlace m3u8")

except Exception as e:
    print("Error:",e)
