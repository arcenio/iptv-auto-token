import requests
import re

pagina = "https://www.cablevisionhd.com/rcn-en-vivo.html"

try:
    respuesta = requests.get(pagina, timeout=20)
    html = respuesta.text

    patron = r'https://[^"]+\.m3u8[^"]*'
    resultado = re.search(patron, html)

    if resultado:
        enlace = resultado.group(0)

        contenido = "#EXTM3U\n"
        contenido += "#EXTINF:-1 tvg-id=\"rcn\" tvg-name=\"RCN\" group-title=\"TV\",RCN En Vivo\n"
        contenido += enlace + "\n"

        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(contenido)

        print("Lista IPTV actualizada correctamente")

    else:
        print("No se encontro enlace m3u8")

except Exception as e:
    print("Error:", e)
