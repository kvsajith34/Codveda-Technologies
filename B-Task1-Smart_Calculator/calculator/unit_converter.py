"""
Unit converter for SmartCalc Pro.
Supported categories: Length, Weight, Temperature, Speed, Area, Data Storage.
"""

# Conversion factors to a common base unit
CONVERSIONS: dict = {
    "📏 Length": {
        "units": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"],
        "to_base": {
            "Meter": 1,
            "Kilometer": 1000,
            "Centimeter": 0.01,
            "Millimeter": 0.001,
            "Mile": 1609.344,
            "Yard": 0.9144,
            "Foot": 0.3048,
            "Inch": 0.0254,
        },
    },
    "⚖️ Weight": {
        "units": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce", "Tonne"],
        "to_base": {
            "Kilogram": 1,
            "Gram": 0.001,
            "Milligram": 0.000001,
            "Pound": 0.453592,
            "Ounce": 0.0283495,
            "Tonne": 1000,
        },
    },
    "🌡️ Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "to_base": None,  # Special handling required
    },
    "💨 Speed": {
        "units": ["m/s", "km/h", "mph", "knot", "ft/s"],
        "to_base": {
            "m/s": 1,
            "km/h": 0.277778,
            "mph": 0.44704,
            "knot": 0.514444,
            "ft/s": 0.3048,
        },
    },
    "📐 Area": {
        "units": ["m²", "km²", "cm²", "ft²", "Acre", "Hectare"],
        "to_base": {
            "m²": 1,
            "km²": 1_000_000,
            "cm²": 0.0001,
            "ft²": 0.092903,
            "Acre": 4046.86,
            "Hectare": 10000,
        },
    },
    "💾 Data": {
        "units": ["Bit", "Byte", "KB", "MB", "GB", "TB"],
        "to_base": {
            "Bit": 0.125,
            "Byte": 1,
            "KB": 1024,
            "MB": 1_048_576,
            "GB": 1_073_741_824,
            "TB": 1_099_511_627_776,
        },
    },
}


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between temperature units via Celsius as intermediate."""
    # Step 1: Convert to Celsius
    if from_unit == "Celsius":
        celsius = value
    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        if value < 0:
            raise ValueError("Kelvin cannot be negative.")
        celsius = value - 273.15

    # Step 2: Convert from Celsius to target
    if to_unit == "Celsius":
        return celsius
    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15


def convert_unit(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Universal unit converter. Returns converted value."""
    if from_unit == to_unit:
        return value

    if category == "🌡️ Temperature":
        return _convert_temperature(value, from_unit, to_unit)

    conv = CONVERSIONS[category]["to_base"]
    base_value = value * conv[from_unit]   # Convert to base unit
    return base_value / conv[to_unit]       # Convert from base to target
