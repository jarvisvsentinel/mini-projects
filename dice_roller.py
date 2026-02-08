import random
import time
import sys

def roll_dice(sides=6, count=1):
    """Rolls 'count' number of 'sides'-sided dice."""
    rolls = [random.randint(1, sides) for _ in range(count)]
    return rolls

def display_rolls(rolls):
    """Prints the results with a bit of flair."""
    print("\nRolling the dice...", end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print("\n")
    
    for i, roll in enumerate(rolls, 1):
        print(f"  Die {i}: [{roll}]")
    
    total = sum(rolls)
    print(f"\nTotal: {total}")
    if total == len(rolls) * 6:
        print("Good heavens! A perfect score!")
    elif total == len(rolls):
        print("Ah, snake eyes... or at least the equivalent. Better luck next time.")

def main():
    print("================================")
    print("   JARVIS'S DELUXE DICE ROLLER  ")
    print("================================")
    
    try:
        sides_input = input("Enter number of sides (default 6): ").strip()
        sides = int(sides_input) if sides_input else 6
        
        count_input = input("Enter number of dice (default 1): ").strip()
        count = int(count_input) if count_input else 1
        
        if sides < 2 or count < 1:
            print("I'm afraid that's physically impossible, sir.")
            return

        rolls = roll_dice(sides, count)
        display_rolls(rolls)
        
    except ValueError:
        print("I'm sorry, I didn't quite catch that number.")
    except KeyboardInterrupt:
        print("\nFarewell then!")

if __name__ == "__main__":
    main()
