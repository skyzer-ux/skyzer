from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ===============================
# DIRECTORY (AMAN DI RENDER)
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Render hanya mengizinkan write di /tmp
LOCATION_DIR = os.path.join("/tmp", "location")
os.makedirs(LOCATION_DIR, exist_ok=True)

# ===============================
# ROUTES
# ===============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_location", methods=["POST"])
def save_location():
    data = request.get_json(silent=True) or {}

    lat = data.get("latitude")
    lon = data.get("longitude")
    timestamp = data.get("timestamp")

    if not lat or not lon or not timestamp:
        return jsonify({"status": "error", "message": "invalid data"}), 400

    # TXT FILE
    file_txt = os.path.join(LOCATION_DIR, "lokasi.txt")
    with open(file_txt, "a", encoding="utf-8") as f:
        f.write(f"📍 {timestamp}\n")
        f.write(f"   Lat: {lat}, Lon: {lon}\n")
        f.write("-" * 25 + "\n")

    # JSON FILE
    file_json = os.path.join(LOCATION_DIR, "current_location.json")
    with open(file_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "latitude": lat,
                "longitude": lon,
                "timestamp": timestamp,
            },
            f,
            indent=4,
            ensure_ascii=False
        )

    return jsonify({"status": "success"})

# ===============================
# RENDER ENTRY POINT
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)