from flask import Flask, jsonify, request
from ytmusicapi import YTMusic
import yt_dlp, os
app = Flask(__name__)
yt = YTMusic()

@app.route("/search")
def buscar():
    q = request.args.get("q", "")
    try:
        r = yt.search(q, filter="songs", limit=20)
        return jsonify([{"titulo": s["title"], "artista": s["artists"][0]["name"], "id": s["videoId"]} for s in r if s.get("videoId")])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stream")
def stream():
    vid = request.args.get("id", "")
    try:
        opts = {"format": "bestaudio/best", "quiet": True, "noplaylist": True, "no_warnings": True,
                "extractor_args": {"youtube": {"player_client": ["android", "web"]}}}
        if os.path.exists("cookies.txt"):
            opts["cookiefile"] = "cookies.txt"
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info("https://www.youtube.com/watch?v=" + vid, download=False)
            url = info.get("url")
            if not url and info.get("formats"):
                for f in reversed(info["formats"]):
                    if f.get("url"): url = f["url"]; break
            return jsonify({"url": url, "titulo": info.get("title", "")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/setcookies", methods=["POST"])
def setcookies():
    try:
        data = request.get_data(as_text=True)
        with open("cookies.txt", "w") as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write(data)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
