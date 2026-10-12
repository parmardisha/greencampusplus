"""Simple, indicative greenhouse-gas estimates for everyday activities."""

CATEGORIES = {
    "electricity": {
        "label": "Electricity",
        "unit": "kWh",
        "factor": 0.42,
        "icon": "⚡",
    },
    "natural_gas": {
        "label": "Natural gas",
        "unit": "kWh",
        "factor": 0.20,
        "icon": "🔥",
    },
    "car": {
        "label": "Car travel",
        "unit": "km",
        "factor": 0.192,
        "icon": "🚗",
    },
    "bus": {
        "label": "Bus travel",
        "unit": "km",
        "factor": 0.105,
        "icon": "🚌",
    },
    "train": {
        "label": "Train travel",
        "unit": "km",
        "factor": 0.041,
        "icon": "🚆",
    },
}


def calculate_emissions(category, amount):
    """Return estimated kilograms of CO2e for a supported activity."""
    if category not in CATEGORIES:
        raise ValueError(f"Unsupported activity category: {category}")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount * CATEGORIES[category]["factor"], 3)
