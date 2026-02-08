#!/usr/bin/env python3
"""
Unit Converter - A versatile command-line unit conversion tool
Supports: Length, Weight, Temperature, Volume, Time, and Data conversions
"""

import sys
from typing import Dict, Tuple, Callable

# Conversion factors (to base unit)
CONVERSIONS = {
    "length": {
        "name": "Length",
        "base": "meters",
        "units": {
            "meters": 1.0,
            "kilometers": 1000.0,
            "centimeters": 0.01,
            "millimeters": 0.001,
            "miles": 1609.344,
            "yards": 0.9144,
            "feet": 0.3048,
            "inches": 0.0254,
        }
    },
    "weight": {
        "name": "Weight",
        "base": "kilograms",
        "units": {
            "kilograms": 1.0,
            "grams": 0.001,
            "milligrams": 0.000001,
            "pounds": 0.453592,
            "ounces": 0.0283495,
            "tons": 1000.0,
        }
    },
    "temperature": {
        "name": "Temperature",
        "special": True,  # Non-linear conversion
    },
    "volume": {
        "name": "Volume",
        "base": "liters",
        "units": {
            "liters": 1.0,
            "milliliters": 0.001,
            "gallons": 3.78541,
            "quarts": 0.946353,
            "pints": 0.473176,
            "cups": 0.236588,
            "fluid_ounces": 0.0295735,
        }
    },
    "time": {
        "name": "Time",
        "base": "seconds",
        "units": {
            "seconds": 1.0,
            "minutes": 60.0,
            "hours": 3600.0,
            "days": 86400.0,
            "weeks": 604800.0,
            "years": 31536000.0,
        }
    },
    "data": {
        "name": "Data",
        "base": "bytes",
        "units": {
            "bytes": 1.0,
            "kilobytes": 1024.0,
            "megabytes": 1048576.0,
            "gigabytes": 1073741824.0,
            "terabytes": 1099511627776.0,
        }
    }
}

def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5/9

def celsius_to_kelvin(c: float) -> float:
    return c + 273.15

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Handle temperature conversions (non-linear)"""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Convert to Celsius first
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = fahrenheit_to_celsius(value)
    elif from_unit == "kelvin":
        celsius = kelvin_to_celsius(value)
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}")
    
    # Convert from Celsius to target
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return celsius_to_fahrenheit(celsius)
    elif to_unit == "kelvin":
        return celsius_to_kelvin(celsius)
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}")

def convert(value: float, from_unit: str, to_unit: str, category: str) -> float:
    """Convert a value from one unit to another within a category"""
    cat_data = CONVERSIONS[category]
    
    # Special handling for temperature
    if cat_data.get("special"):
        return convert_temperature(value, from_unit, to_unit)
    
    # Linear conversions
    units = cat_data["units"]
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit not in units:
        raise ValueError(f"Unknown unit: {from_unit}")
    if to_unit not in units:
        raise ValueError(f"Unknown unit: {to_unit}")
    
    # Convert to base unit, then to target unit
    base_value = value * units[from_unit]
    result = base_value / units[to_unit]
    
    return result

def list_categories():
    """Display all available conversion categories"""
    print("\n🔧 Available Conversion Categories:")
    print("=" * 50)
    for key, data in CONVERSIONS.items():
        print(f"  • {data['name'].upper()} ({key})")
    print()

def list_units(category: str):
    """Display all units in a category"""
    if category not in CONVERSIONS:
        print(f"❌ Unknown category: {category}")
        return
    
    cat_data = CONVERSIONS[category]
    print(f"\n📏 {cat_data['name']} Units:")
    print("=" * 50)
    
    if category == "temperature":
        print("  • Celsius")
        print("  • Fahrenheit")
        print("  • Kelvin")
    else:
        for unit in cat_data["units"].keys():
            print(f"  • {unit.capitalize()}")
    print()

def interactive_mode():
    """Run the converter in interactive mode"""
    print("\n" + "=" * 60)
    print("🎯 UNIT CONVERTER - Interactive Mode")
    print("=" * 60)
    
    list_categories()
    
    category = input("Select category (or 'quit' to exit): ").strip().lower()
    
    if category in ["quit", "exit", "q"]:
        print("👋 Goodbye!")
        return
    
    if category not in CONVERSIONS:
        print(f"❌ Invalid category: {category}")
        return interactive_mode()
    
    list_units(category)
    
    try:
        value = float(input("Enter value to convert: ").strip())
        from_unit = input("From unit: ").strip().lower()
        to_unit = input("To unit: ").strip().lower()
        
        result = convert(value, from_unit, to_unit, category)
        
        print("\n" + "=" * 60)
        print(f"✅ RESULT: {value} {from_unit} = {result:.6f} {to_unit}")
        print("=" * 60 + "\n")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Ask if they want to continue
    again = input("Convert another? (y/n): ").strip().lower()
    if again in ["y", "yes"]:
        interactive_mode()
    else:
        print("👋 Goodbye!")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_mode()
    elif len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        print("\nUsage:")
        print("  Interactive mode: python converter.py")
        print("  Direct mode:      python converter.py <value> <from_unit> <to_unit> <category>")
        print("\nExample:")
        print("  python converter.py 100 kilometers miles length")
        print("  python converter.py 32 fahrenheit celsius temperature")
    elif len(sys.argv) == 5:
        # Direct mode
        try:
            value = float(sys.argv[1])
            from_unit = sys.argv[2].lower()
            to_unit = sys.argv[3].lower()
            category = sys.argv[4].lower()
            
            result = convert(value, from_unit, to_unit, category)
            print(f"{value} {from_unit} = {result:.6f} {to_unit}")
        except ValueError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        print("❌ Invalid arguments. Use -h for help.")
        sys.exit(1)

if __name__ == "__main__":
    main()
