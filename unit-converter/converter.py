def convert_length(value, from_unit, to_unit):
    # Base unit: meters
    length_factors = {
        'm': 1,
        'km': 1000,
        'cm': 0.01,
        'mm': 0.001,
        'mi': 1609.34,
        'yd': 0.9144,
        'ft': 0.3048,
        'in': 0.0254
    }
    
    if from_unit not in length_factors or to_unit not in length_factors:
        return None
        
    meters = value * length_factors[from_unit]
    return meters / length_factors[to_unit]

def convert_weight(value, from_unit, to_unit):
    # Base unit: kilograms
    weight_factors = {
        'kg': 1,
        'g': 0.001,
        'mg': 0.000001,
        'lb': 0.453592,
        'oz': 0.0283495
    }
    
    if from_unit not in weight_factors or to_unit not in weight_factors:
        return None
        
    kg = value * weight_factors[from_unit]
    return kg / weight_factors[to_unit]

def convert_temp(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    celsius = 0
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    else:
        return None
        
    # Convert from Celsius to target
    if to_unit == 'C':
        return celsius
    elif to_unit == 'F':
        return (celsius * 9/5) + 32
    elif to_unit == 'K':
        return celsius + 273.15
    else:
        return None

def main():
    print("=== Python Unit Converter ===")
    print("1. Length (m, km, cm, mm, mi, yd, ft, in)")
    print("2. Weight (kg, g, mg, lb, oz)")
    print("3. Temperature (C, F, K)")
    
    try:
        choice = input("Select category (1-3): ")
        if choice not in ['1', '2', '3']:
            print("Invalid selection.")
            return

        val = float(input("Enter value: "))
        from_u = input("From unit: ")
        to_u = input("To unit: ")
        
        result = None
        if choice == '1':
            result = convert_length(val, from_u, to_u)
        elif choice == '2':
            result = convert_weight(val, from_u, to_u)
        elif choice == '3':
            result = convert_temp(val, from_u, to_u)
            
        if result is not None:
            print(f"{val} {from_u} = {result:.4f} {to_u}")
        else:
            print("Invalid unit conversion.")
            
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
