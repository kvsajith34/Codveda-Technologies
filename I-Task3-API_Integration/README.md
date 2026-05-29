# 🌤️ Weather CLI App

A command-line weather application built in Python that fetches real-time weather data and a 5-day forecast for any city in the world — no API key required.

---

## 📸 Screenshots

**London**
```
════════════════════════════════════════════════════
  📍 London, England, United Kingdom
  🕐 2026-05-29  17:15
════════════════════════════════════════════════════

  ⛅  Partly cloudy

  Temperature          26.0 °C
  Feels Like           23.4 °C
  Humidity             30 %
  Precipitation        0.0 mm
  Wind                 13.0 km/h  WNW  (298°)
  Pressure             1018.9 hPa
  Visibility           26 km

  ────────────────────────────────────────────────
                    5-DAY FORECAST
  ────────────────────────────────────────────────
  Date         Condition                High   Low    Rain
  ────────────────────────────────────────────────
  Today        ☁️ Overcast              26.3°  18.9°   0.0 mm
  Tomorrow     ☁️ Overcast              27.5°  17.6°   0.0 mm
  Sun, 31 May  ☁️ Overcast              22.1°  16.7°   0.0 mm
  Mon, 01 Jun  🌦️ Light drizzle         21.5°  14.1°   0.4 mm
  Tue, 02 Jun  🌧️ Slight rain           20.5°  15.0°  17.6 mm
  ────────────────────────────────────────────────

  Data provided by Open-Meteo (open-meteo.com)
```

---

## 🚀 Features

- **Current conditions** — temperature, feels like, humidity, precipitation, wind speed & direction, pressure, visibility
- **5-day forecast** — daily high/low, condition, and rainfall
- **Auto-timezone** — displays local time for the queried city
- **CLI argument or interactive prompt** — flexible input modes
- **No API key** — powered entirely by the free [Open-Meteo](https://open-meteo.com) API
- **Full error handling** — invalid cities, network failures, timeouts, and unexpected responses

---

## 🛠️ Tech Stack

| Component       | Details                                      |
|-----------------|----------------------------------------------|
| Language        | Python 3.10+                                 |
| HTTP Requests   | `requests`                                   |
| Weather API     | [Open-Meteo Forecast API](https://open-meteo.com/en/docs) |
| Geocoding API   | [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) |

---

## 📦 Installation

```bash
# 1. Clone or download the project
git clone https://github.com/kvsajith34/Codveda-Technologies.git
cd I-Task3-API_Integration

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

**Pass the city as a command-line argument:**
```bash
python weather_app.py London
python weather_app.py "New York"
python weather_app.py Tokyo
```

**Or run without arguments for an interactive prompt:**
```bash
python weather_app.py
Enter city name: Hyderabad
```

---

## 🗂️ Project Structure

```
weather-cli/
├── weather_app.py      # Main application (single-file)
└── requirements.txt    # Python dependencies
└── README.md           # Project Documentation & Instructions 
```

---

## ⚙️ How It Works

```
User Input (city name)
        │
        ▼
┌───────────────────┐
│  Geocoding API    │  Resolves city → latitude, longitude, timezone
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Weather API      │  Fetches current conditions + 5-day daily forecast
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  Parse & Display  │  Formats JSON → readable CLI output
└───────────────────┘
```

---

## 🔒 Error Handling

| Scenario                   | Behaviour                                      |
|----------------------------|------------------------------------------------|
| City not found             | `✗  City "xyz" not found. Try a different spelling.` |
| No internet connection     | `✗  No internet connection. Please check your network.` |
| Request timeout            | `✗  Request timed out. The server is not responding.` |
| HTTP / API error           | Displays the HTTP status code and reason       |
| Unexpected API response    | `✗  Unexpected API response. Could not parse weather data.` |
| Empty city input           | `✗  Please provide a city name.`              |

---

## 📋 Requirements

```
requests>=2.28.0
```

---

## 📄 License

This project is open-source and available under the [MIT License]

---

## 🙏 Credits

Weather data provided by **[Open-Meteo](https://open-meteo.com)** — a free, open-source weather API with no registration or API key required.