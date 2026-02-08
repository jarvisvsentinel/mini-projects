# 🔄 Universal Unit Converter

A comprehensive command-line unit conversion tool supporting 6 categories and 40+ units.

## Features

- **6 Conversion Categories:**
  - 📏 Length (mm, cm, m, km, inch, foot, yard, mile)
  - ⚖️ Weight (mg, g, kg, ton, oz, lb, stone)
  - 🌡️ Temperature (Celsius, Fahrenheit, Kelvin)
  - 🧪 Volume (ml, l, gallon, quart, pint, cup, fl_oz)
  - ⏱️ Time (ms, s, min, hour, day, week, year)
  - 🚀 Speed (mps, kph, mph, knot)

- **Two Usage Modes:**
  - Interactive menu-driven interface
  - Quick command-line conversion

- **Smart Features:**
  - Input validation
  - High-precision results (6 decimal places)
  - Friendly error messages
  - Clean, colorful output

## Installation

```bash
chmod +x converter.py
```

## Usage

### Interactive Mode

```bash
./converter.py
```

Follow the menu to:
1. Select a category
2. Enter the value to convert
3. Specify source and target units

### Quick Mode

```bash
./converter.py <value> <from_unit> <to_unit> <category>
```

**Examples:**

```bash
# Convert 100 kilometers to miles
./converter.py 100 km mile length

# Convert 32 Fahrenheit to Celsius
./converter.py 32 f c temperature

# Convert 5 pounds to kilograms
./converter.py 5 lb kg weight

# Convert 1 gallon to liters
./converter.py 1 gallon l volume

# Convert 60 mph to kph
./converter.py 60 mph kph speed
```

## Unit Reference

### Length
`mm` `cm` `m` `km` `inch` `foot` `yard` `mile`

### Weight
`mg` `g` `kg` `ton` `oz` `lb` `stone`

### Temperature
`c` (Celsius) `f` (Fahrenheit) `k` (Kelvin)

### Volume
`ml` `l` `gallon` `quart` `pint` `cup` `fl_oz`

### Time
`ms` `s` `min` `hour` `day` `week` `year`

### Speed
`mps` (meters/sec) `kph` (km/hour) `mph` (miles/hour) `knot`

## Examples

```
$ ./converter.py

==================================================
🔄 Universal Unit Converter
==================================================

Available Categories:
  1. Length
  2. Weight
  3. Temperature
  4. Volume
  5. Time
  6. Speed
  0. Exit

Select category (0-6): 1

📏 Length Units:
          mm  |          cm  |           m  |          km
        inch  |        foot  |        yard  |        mile

Enter value to convert: 100
From unit: km
To unit: mile

✅ Result: 100 km = 62.137119 mile
```

## Why This Converter?

- ✨ **Comprehensive**: 40+ units across 6 categories
- 🎯 **Accurate**: Precise conversion ratios
- 🚀 **Fast**: Both interactive and CLI modes
- 🧹 **Clean**: Well-organized, readable code
- 🛡️ **Robust**: Input validation and error handling

## Dependencies

- Python 3.6+
- No external packages required (uses only standard library)

## Author

Built by Jarvis 🎩 (2026-02-08)

## License

Free to use and modify!
