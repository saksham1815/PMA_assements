from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_url_path='/static')

API_KEY = "0cb301f536407c2a042a7247e72e955a"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def get_weather():
    print("Received weather request")
    try:
        data = request.get_json()
        location = data.get("location")
        lat = data.get("lat")
        lon = data.get("lon")

        if location:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        else:
            return jsonify({"error": "Location required"}), 400

        weather = requests.get(url).json()
        forecast = requests.get(forecast_url).json()

        if "weather" not in weather or "list" not in forecast:
            return jsonify({"error": "Invalid location or no data found"}), 404

        return jsonify({"current": weather, "forecast": forecast})

    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": "Server error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
