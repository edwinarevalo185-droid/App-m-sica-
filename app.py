from flask import Flask, jsonify, request
from ytmusicapi import YTMusic
import yt_dlp
app = Flask(__name__)
yt = YTMusic()

@app.route("/search")
def buscar():
    q = request.args.get("q", "")
    r = yt.search(q, filter="songs", limit=20)
    return jsonify([{"titulo": s["title"], "artista": s["artists"][0]["name"], "id": s["videoId"]} for s in r if s.get("videoId")])

@app.route("/stream")
def stream():
    vid = request.args.get("id", "")
    with yt_dlp.YoutubeDL({"format":"bestaudio","quiet":True}) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v="+vid, download=False)
        return jsonify({"url": info["url"], "titulo": info["title"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
