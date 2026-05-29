"""
Weather CLI App — Open-Meteo API (no API key required)
Uses: Geocoding API + Weather Forecast API from open-meteo.com
"""

import sys
import requests
from datetime import datetime, timedelta

# ─── Constants ────────────────────────────────────────────────────────────────

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT     = 10  # seconds

# WMO Weather Interpretation Codes → (description, emoji)
WMO_CODES = {
    0:  ("Clear sky",                    "☀️"),
    1:  ("Mainly clear",                 "🌤️"),
    2:  ("Partly cloudy",                "⛅"),
    3:  ("Overcast",                     "☁️"),
    45: ("Foggy",                        "🌫️"),
    48: ("Icy fog",                      "🌫️"),
    51: ("Light drizzle",                "🌦️"),
    53: ("Moderate drizzle",             "🌦️"),
    55: ("Dense drizzle",                "🌧️"),
    61: ("Slight rain",                  "🌧️"),
    63: ("Moderate rain",                "🌧️"),
    65: ("Heavy rain",                   "🌧️"),
    71: ("Slight snow",                  "🌨️"),
    73: ("Moderate snow",                "🌨️"),
    75: ("Heavy snow",                   "❄️"),
    77: ("Snow grains",                  "❄️"),
    80: ("Slight showers",               "🌦️"),
    81: ("Moderate showers",             "🌧️"),
    82: ("Violent showers",              "⛈️"),
    85: ("Slight snow showers",          "🌨️"),
    86: ("Heavy snow showers",           "❄️"),
    95: ("Thunderstorm",                 "⛈️"),
    96: ("Thunderstorm w/ slight hail",  "⛈️"),
    99: ("Thunderstorm w/ heavy hail",   "⛈️"),
}

WIND_DIRECTIONS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]

# ─── API Calls ────────────────────────────────────────────────────────────────

def get_coordinates(city: str) -> dict:
    """Resolve a city name to lat/lon using the Open-Meteo Geocoding API."""
    params = {"name": city, "count": 1, "language": "en", "format": "json"}

    try:
        response = requests.get(GEOCODE_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise SystemExit("✗  No internet connection. Please check your network.")
    except requests.exceptions.Timeout:
        raise SystemExit("✗  Request timed out. The geocoding server is not responding.")
    except requests.exceptions.HTTPError as e:
        raise SystemExit(f"✗  Geocoding API error: {e}")

    data = response.json()
    results = data.get("results")

    if not results:
        raise SystemExit(f'✗  City "{city}" not found. Try a different spelling or a nearby city.')

    loc = results[0]
    return {
        "latitude":  loc["latitude"],
        "longitude": loc["longitude"],
        "name":      loc["name"],
        "country":   loc.get("country", ""),
        "admin1":    loc.get("admin1", ""),  # state / region
        "timezone":  loc.get("timezone", "auto"),
    }


def get_weather(lat: float, lon: float, timezone: str) -> dict:
    """Fetch current conditions and a 5-day daily forecast from Open-Meteo."""
    params = {
        "latitude":  lat,
        "longitude": lon,
        "timezone":  timezone,
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weathercode",
            "wind_speed_10m",
            "wind_direction_10m",
            "surface_pressure",
            "visibility",
        ]),
        "daily": ",".join([
            "weathercode",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
        ]),
        "wind_speed_unit": "kmh",
        "forecast_days":   5,
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise SystemExit("✗  No internet connection. Please check your network.")
    except requests.exceptions.Timeout:
        raise SystemExit("✗  Request timed out. The weather server is not responding.")
    except requests.exceptions.HTTPError as e:
        raise SystemExit(f"✗  Weather API error: {e}")

    data = response.json()

    if "current" not in data:
        raise SystemExit("✗  Unexpected API response. Could not parse weather data.")

    return data

# ─── Helpers ──────────────────────────────────────────────────────────────────

def decode_wmo(code: int) -> tuple[str, str]:
    """Return (description, emoji) for a WMO weather code."""
    return WMO_CODES.get(code, ("Unknown conditions", "🌡️"))


def wind_direction_label(degrees: float) -> str:
    """Convert wind bearing (0–360°) to a compass label."""
    index = round(degrees / 22.5) % 16
    return WIND_DIRECTIONS[index]


def format_date(date_str: str) -> str:
    """Format 'YYYY-MM-DD' → 'Mon, 02 Jun'."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    today    = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    if dt.date() == today:
        return "Today     "
    if dt.date() == tomorrow:
        return "Tomorrow  "
    return dt.strftime("%a, %d %b")


def separator(char: str = "─", width: int = 52) -> str:
    return char * width

# ─── Display ──────────────────────────────────────────────────────────────────

def display_weather(weather: dict, location: dict) -> None:
    """Render current conditions and the 5-day forecast to stdout."""

    cur   = weather["current"]
    daily = weather["daily"]
    units = weather["current_units"]

    temp       = cur["temperature_2m"]
    feels_like = cur["apparent_temperature"]
    humidity   = cur["relative_humidity_2m"]
    precip     = cur["precipitation"]
    wind_spd   = cur["wind_speed_10m"]
    wind_deg   = cur["wind_direction_10m"]
    pressure   = cur.get("surface_pressure", "N/A")
    visibility = cur.get("visibility")
    wmo_code   = cur["weathercode"]

    desc, emoji = decode_wmo(wmo_code)
    wind_dir    = wind_direction_label(wind_deg)
    vis_str     = f"{int(visibility/1000)} km" if visibility is not None else "N/A"

    # Location header
    region = f", {location['admin1']}" if location["admin1"] else ""
    full_location = f"{location['name']}{region}, {location['country']}"

    print()
    print(separator("═"))
    print(f"  📍 {full_location}")
    print(f"  🕐 {cur['time'].replace('T', '  ')}")
    print(separator("═"))

    # Current conditions
    print(f"\n  {emoji}  {desc}")
    print(f"\n  {'Temperature':<20} {temp} {units['temperature_2m']}")
    print(f"  {'Feels Like':<20} {feels_like} {units['apparent_temperature']}")
    print(f"  {'Humidity':<20} {humidity} {units['relative_humidity_2m']}")
    print(f"  {'Precipitation':<20} {precip} {units['precipitation']}")
    print(f"  {'Wind':<20} {wind_spd} {units['wind_speed_10m']}  {wind_dir}  ({wind_deg}°)")
    print(f"  {'Pressure':<20} {pressure} hPa")
    print(f"  {'Visibility':<20} {vis_str}")

    # 5-day forecast
    print(f"\n  {separator('─', 48)}")
    print(f"  {'5-DAY FORECAST':^48}")
    print(f"  {separator('─', 48)}")
    print(f"  {'Date':<12} {'Condition':<24} {'High':>5}  {'Low':>5}  {'Rain':>6}")
    print(f"  {separator('─', 48)}")

    for i, date_str in enumerate(daily["time"]):
        day_code        = daily["weathercode"][i]
        day_desc, d_emo = decode_wmo(day_code)
        t_max           = daily["temperature_2m_max"][i]
        t_min           = daily["temperature_2m_min"][i]
        rain            = daily["precipitation_sum"][i]
        label           = format_date(date_str)
        condition_str   = f"{d_emo} {day_desc}"

        print(f"  {label:<12} {condition_str:<24} {t_max:>4}°  {t_min:>4}°  {rain:>5} mm")

    print(f"  {separator('─', 48)}")
    print(f"\n  Data provided by Open-Meteo (open-meteo.com)\n")

# ─── Entry Point ──────────────────────────────────────────────────────────────

def main() -> None:
    # Accept city from CLI arg or interactive prompt
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:]).strip()
    else:
        try:
            city = input("Enter city name: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(0)

    if not city:
        raise SystemExit("✗  Please provide a city name.")

    location = get_coordinates(city)
    weather  = get_weather(location["latitude"], location["longitude"], location["timezone"])
    display_weather(weather, location)


if __name__ == "__main__":
    main()
