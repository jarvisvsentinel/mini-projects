#!/usr/bin/env python3
"""
Universal Unit Converter
A comprehensive CLI tool for converting between various units
"""

import sys
from typing import Dict, Callable

# Conversion functions
def length_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between length units"""
    to_meters = {
        'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000,
        'inch': 0.0254, 'foot': 0.3048, 'yard': 0.9144, 'mile': 1609.34
    }
    return value * to_meters[from_unit] / to_meters[to_unit]

def weight_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between weight units"""
    to_kg = {
        'mg': 0.000001, 'g': 0.001, 'kg': 1, 'ton': 1000,
        'oz': 0.0283495, 'lb': 0.453592, 'stone': 6.35029
    }
    return value * to_kg[from_unit] / to_kg[to_unit]

def temperature_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between temperature units"""
    # Convert to Celsius first
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5/9
    elif from_unit == 'k':
        celsius = value - 273.15
    
    # Convert from Celsius to target
    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return celsius * 9/5 + 32
    elif to_unit == 'k':
        return celsius + 273.15

def volume_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between volume units"""
    to_liters = {
        'ml': 0.001, 'l': 1, 'gallon': 3.78541, 'quart': 0.946353,
        'pint': 0.473176, 'cup': 0.236588, 'fl_oz': 0.0295735
    }
    return value * to_liters[from_unit] / to_liters[to_unit]

def time_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between time units"""
    to_seconds = {
        'ms': 0.001, 's': 1, 'min': 60, 'hour': 3600,
        'day': 86400, 'week': 604800, 'year': 31536000
    }
    return value * to_seconds[from_unit] / to_seconds[to_unit]

def speed_converter(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between speed units"""
    to_mps = {
        'mps': 1, 'kph': 0.277778, 'mph': 0.44704, 'knot': 0.514444
    }
    return value * to_mps[from_unit] / to_mps[to_unit]

# Category definitions
CATEGORIES = {
    'length': {
        'name': 'Length',
        'units': ['mm', 'cm', 'm', 'km', 'inch', 'foot', 'yard', 'mile'],
        'converter': length_converter
    },
    'weight': {
        'name': 'Weight',
        'units': ['mg', 'g', 'kg', 'ton', 'oz', 'lb', 'stone'],
        'converter': weight_converter
    },
    'temperature': {
        'name': 'Temperature',
        'units': ['c', 'f', 'k'],
        'converter': temperature_converter
    },
    'volume': {
        'name': 'Volume',
        'units': ['ml', 'l', 'gallon', 'quart', 'pint', 'cup', 'fl_oz'],
        'converter': volume_converter
    },
    'time': {
        'name': 'Time',
        'units': ['ms', 's', 'min', 'hour', 'day', 'week', 'year'],
        'converter': time_converter
    },
    'speed': {
        'name': 'Speed',
        'units': ['mps', 'kph', 'mph', 'knot'],
        'converter': speed_converter
    }
}

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🔄 Universal Unit Converter")
    print("="*50)
    print("\nAvailable Categories:")
    for idx, (key, cat) in enumerate(CATEGORIES.items(), 1):
        print(f"  {idx}. {cat['name']}")
    print("  0. Exit")
    print()

def show_units(category: str):
    """Display available units for a category"""
    cat_data = CATEGORIES[category]
    print(f"\n📏 {cat_data['name']} Units:")
    units = cat_data['units']
    for i in range(0, len(units), 4):
        row = units[i:i+4]
        print("  " + "  |  ".join(f"{u:>10}" for u in row))
    print()

def convert(category: str):
    """Perform conversion for a category"""
    cat_data = CATEGORIES[category]
    show_units(category)
    
    try:
        value = float(input("Enter value to convert: "))
        from_unit = input("From unit: ").strip().lower()
        to_unit = input("To unit: ").strip().lower()
        
        if from_unit not in cat_data['units'] or to_unit not in cat_data['units']:
            print("❌ Invalid unit(s)!")
            return
        
        result = cat_data['converter'](value, from_unit, to_unit)
        print(f"\n✅ Result: {value} {from_unit} = {result:.6f} {to_unit}")
        
    except ValueError:
        print("❌ Invalid number!")
    except KeyError:
        print("❌ Unit not supported!")
    except Exception as e:
        print(f"❌ Error: {e}")

def quick_convert(args):
    """Quick conversion from command line arguments"""
    if len(args) != 4:
        print("Usage: converter.py <value> <from_unit> <to_unit> <category>")
        print("Example: converter.py 100 km mile length")
        sys.exit(1)
    
    value = float(args[0])
    from_unit = args[1].lower()
    to_unit = args[2].lower()
    category = args[3].lower()
    
    if category not in CATEGORIES:
        print(f"❌ Unknown category: {category}")
        print(f"Available: {', '.join(CATEGORIES.keys())}")
        sys.exit(1)
    
    cat_data = CATEGORIES[category]
    result = cat_data['converter'](value, from_unit, to_unit)
    print(f"{value} {from_unit} = {result:.6f} {to_unit}")

def main():
    """Main interactive loop"""
    if len(sys.argv) > 1:
        quick_convert(sys.argv[1:])
        return
    
    while True:
        show_menu()
        try:
            choice = input("Select category (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 Thanks for using Unit Converter!")
                break
            
            try:
                idx = int(choice) - 1
                categories = list(CATEGORIES.keys())
                if 0 <= idx < len(categories):
                    convert(categories[idx])
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Please enter a number!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
