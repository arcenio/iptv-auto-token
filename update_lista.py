from flask import Flask, Response
import requests

app = Flask(__name__)

STREAM_URL = "https://regionales.saohgdasregions.fun:9092/MTkwLjIxOS4xNDQuMzY=/18_.m3u8"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cablevisionhd.com/",
    "Origin": "https://www.cablevisionhd.com"
}

@app.route("/rcn.m3u8")
def proxy():
    r = requests.get(STREAM_URL, headers=HEADERS, stream=True)

    return Response(
        r.iter_content(chunk_size=1024),
        content_type=r.headers.get("Content-Type")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
