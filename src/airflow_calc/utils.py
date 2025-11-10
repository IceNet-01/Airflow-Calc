"""
Utility functions for airflow calculations and formatting
"""

import json
from typing import Dict, Any


def format_large_number(number, decimals=2):
    """Format large numbers with appropriate units"""
    if abs(number) >= 1e6:
        return f"{number/1e6:.{decimals}f}M"
    elif abs(number) >= 1e3:
        return f"{number/1e3:.{decimals}f}K"
    else:
        return f"{number:.{decimals}f}"


def mph_to_ms(mph):
    """Convert miles per hour to meters per second"""
    return mph * 0.44704


def ms_to_mph(ms):
    """Convert meters per second to miles per hour"""
    return ms * 2.23694


def kmh_to_ms(kmh):
    """Convert kilometers per hour to meters per second"""
    return kmh / 3.6


def ms_to_kmh(ms):
    """Convert meters per second to kilometers per hour"""
    return ms * 3.6


def feet_to_meters(feet):
    """Convert feet to meters"""
    return feet * 0.3048


def meters_to_feet(meters):
    """Convert meters to feet"""
    return meters * 3.28084


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9


def print_section_header(title, width=60):
    """Print a formatted section header"""
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_result_table(data: Dict[str, Any], indent=0):
    """Print results in a formatted table"""
    indent_str = " " * indent

    for key, value in data.items():
        # Format key (convert underscore to spaces and title case)
        formatted_key = key.replace("_", " ").title()

        if isinstance(value, dict):
            print(f"{indent_str}{formatted_key}:")
            print_result_table(value, indent + 2)
        elif isinstance(value, float):
            # Format floats with appropriate precision
            if abs(value) < 0.01 and value != 0:
                print(f"{indent_str}{formatted_key}: {value:.6e}")
            elif abs(value) >= 1000:
                print(f"{indent_str}{formatted_key}: {value:,.2f}")
            else:
                print(f"{indent_str}{formatted_key}: {value:.4f}")
        else:
            print(f"{indent_str}{formatted_key}: {value}")


def export_to_json(data: Dict[str, Any], filename: str):
    """Export data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"\nResults exported to: {filename}")


def create_ascii_graph(values, labels, width=50, height=10, title="Graph"):
    """Create a simple ASCII graph"""
    if not values or not labels:
        return "No data to plot"

    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val if max_val != min_val else 1

    lines = [title, "─" * width]

    # Create horizontal bars
    for label, value in zip(labels, values):
        bar_length = int(((value - min_val) / range_val) * (width - 20))
        bar = "█" * bar_length
        lines.append(f"{label:12s} │{bar} {value:.2f}")

    lines.append("─" * width)

    return "\n".join(lines)


def validate_positive_number(value, name="value"):
    """Validate that a number is positive"""
    try:
        num = float(value)
        if num < 0:
            raise ValueError(f"{name} must be positive")
        return num
    except ValueError as e:
        raise ValueError(f"Invalid {name}: {e}")


def validate_speed(speed_ms, unit="m/s"):
    """Validate speed value"""
    if speed_ms < 0:
        raise ValueError("Speed cannot be negative")
    if speed_ms > 150:  # ~540 km/h, ~335 mph
        print(f"Warning: Speed {speed_ms} m/s ({ms_to_kmh(speed_ms):.1f} km/h) is unusually high")
    return speed_ms


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def disable():
        """Disable colors"""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.END = ''


def format_colored(text, color):
    """Format text with color"""
    return f"{color}{text}{Colors.END}"
