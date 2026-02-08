# 🔧 Unit Converter

A versatile command-line unit conversion tool supporting multiple conversion categories with both interactive and direct modes.

## ✨ Features

- **6 Conversion Categories:**
  - 📏 Length (meters, kilometers, miles, feet, inches, etc.)
  - ⚖️ Weight (kilograms, grams, pounds, ounces, etc.)
  - 🌡️ Temperature (Celsius, Fahrenheit, Kelvin)
  - 🧪 Volume (liters, gallons, cups, fluid ounces, etc.)
  - ⏰ Time (seconds, minutes, hours, days, weeks, years)
  - 💾 Data (bytes, kilobytes, megabytes, gigabytes, terabytes)

- **Dual Operating Modes:**
  - Interactive mode with guided prompts
  - Direct command-line mode for scripting

- **High Precision:** Results displayed with 6 decimal places

## 🚀 Usage

### Interactive Mode (Recommended)

Simply run the script without arguments:

```bash
python converter.py
```

You'll be guided through:
1. Selecting a conversion category
2. Entering the value to convert
3. Specifying source and target units
4. Option to perform multiple conversions

### Direct Mode

For quick conversions or scripting:

```bash
python converter.py <value> <from_unit> <to_unit> <category>
```

**Examples:**

```bash
# Convert 100 kilometers to miles
python converter.py 100 kilometers miles length

# Convert 32°F to Celsius
python converter.py 32 fahrenheit celsius temperature

# Convert 5 pounds to kilograms
python converter.py 5 pounds kilograms weight

# Convert 2 gigabytes to megabytes
python converter.py 2 gigabytes megabytes data

# Convert 3 hours to seconds
python converter.py 3 hours seconds time
```

### Help

```bash
python converter.py --help
```

## 📋 Supported Units

### Length
- meters, kilometers, centimeters, millimeters
- miles, yards, feet, inches

### Weight
- kilograms, grams, milligrams
- pounds, ounces, tons

### Temperature
- Celsius, Fahrenheit, Kelvin

### Volume
- liters, milliliters
- gallons, quarts, pints, cups, fluid_ounces

### Time
- seconds, minutes, hours, days, weeks, years

### Data
- bytes, kilobytes, megabytes, gigabytes, terabytes

## 🎯 Examples

```
$ python converter.py

🎯 UNIT CONVERTER - Interactive Mode
============================================================

🔧 Available Conversion Categories:
==================================================
  • LENGTH (length)
  • WEIGHT (weight)
  • TEMPERATURE (temperature)
  • VOLUME (volume)
  • TIME (time)
  • DATA (data)

Select category (or 'quit' to exit): temperature

📏 Temperature Units:
==================================================
  • Celsius
  • Fahrenheit
  • Kelvin

Enter value to convert: 100
From unit: celsius
To unit: fahrenheit

============================================================
✅ RESULT: 100.0 celsius = 212.000000 fahrenheit
============================================================
```

## 🔥 Why This Converter?

- **Comprehensive:** Covers all common conversion needs in one tool
- **Accurate:** Uses precise conversion factors
- **User-Friendly:** Clear prompts and colorful emoji indicators
- **Flexible:** Works both interactively and in scripts
- **Temperature-Smart:** Handles non-linear temperature conversions correctly

## 📦 Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 🎨 Future Enhancements

Potential additions:
- Currency conversion (with API)
- Speed conversions (mph, km/h, knots)
- Pressure conversions (psi, bar, atm)
- Energy conversions (joules, calories, BTU)
- Configuration file for custom units

## 📝 License

Free to use, modify, and distribute. Built with 🎩 by Jarvis.

---

**Pro Tip:** Bookmark this in your terminal with an alias:
```bash
alias convert='python /path/to/converter.py'
```

Then just type `convert` anytime!
