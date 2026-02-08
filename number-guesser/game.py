#!/usr/bin/env python3
"""
Number Guesser - A fun number guessing game with personality!
"""

import random
import sys
from datetime import datetime

class NumberGuesser:
    def __init__(self):
        self.games_played = 0
        self.total_guesses = 0
        self.best_score = None
        
    def play_game(self, min_num=1, max_num=100):
        """Play a single round of the guessing game."""
        secret_number = random.randint(min_num, max_num)
        guesses = 0
        
        print(f"\n🎯 I'm thinking of a number between {min_num} and {max_num}...")
        print("Can you guess it? (Type 'quit' to exit)\n")
        
        while True:
            try:
                user_input = input("Your guess: ").strip().lower()
                
                if user_input == 'quit':
                    print(f"\n👋 Giving up? The number was {secret_number}!")
                    return None
                
                guess = int(user_input)
                guesses += 1
                
                if guess < min_num or guess > max_num:
                    print(f"❌ That's outside the range! Pick between {min_num} and {max_num}.")
                    continue
                
                if guess < secret_number:
                    diff = secret_number - guess
                    if diff > 20:
                        print("📉 Way too low! Think bigger!")
                    elif diff > 10:
                        print("📉 Too low! Getting warmer though...")
                    else:
                        print("📉 Close! Just a bit higher!")
                        
                elif guess > secret_number:
                    diff = guess - secret_number
                    if diff > 20:
                        print("📈 Way too high! Think smaller!")
                    elif diff > 10:
                        print("📈 Too high! You're in the zone...")
                    else:
                        print("📈 So close! Just a tad lower!")
                        
                else:
                    # Winner!
                    self.games_played += 1
                    self.total_guesses += guesses
                    
                    print(f"\n🎉 CORRECT! You got it in {guesses} guess{'es' if guesses != 1 else ''}!")
                    
                    if self.best_score is None or guesses < self.best_score:
                        self.best_score = guesses
                        if guesses == 1:
                            print("🏆 LEGENDARY! First try! Are you psychic?!")
                        else:
                            print(f"🏆 NEW PERSONAL BEST!")
                    
                    if guesses <= 3:
                        print("🔥 Incredible! You're a natural!")
                    elif guesses <= 7:
                        print("👍 Nice work! Solid performance!")
                    elif guesses <= 15:
                        print("😊 Not bad! Keep practicing!")
                    else:
                        print("🤔 You got there eventually!")
                    
                    return guesses
                    
            except ValueError:
                print("⚠️  Please enter a valid number (or 'quit').")
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted! Thanks for playing!")
                sys.exit(0)
    
    def show_stats(self):
        """Display game statistics."""
        if self.games_played == 0:
            print("\n📊 No games played yet!")
            return
        
        avg_guesses = self.total_guesses / self.games_played
        
        print("\n" + "="*40)
        print("📊 YOUR STATS")
        print("="*40)
        print(f"Games Played:    {self.games_played}")
        print(f"Total Guesses:   {self.total_guesses}")
        print(f"Average Guesses: {avg_guesses:.1f}")
        print(f"Best Score:      {self.best_score} guess{'es' if self.best_score != 1 else ''}")
        print("="*40 + "\n")
    
    def difficulty_menu(self):
        """Let the player choose difficulty."""
        print("\n🎮 Choose your difficulty:")
        print("  1. Easy (1-50)")
        print("  2. Medium (1-100)")
        print("  3. Hard (1-500)")
        print("  4. Insane (1-1000)")
        
        while True:
            choice = input("\nDifficulty [1-4]: ").strip()
            
            if choice == '1':
                return 1, 50
            elif choice == '2':
                return 1, 100
            elif choice == '3':
                return 1, 500
            elif choice == '4':
                return 1, 1000
            else:
                print("Invalid choice! Pick 1-4.")
    
    def main_menu(self):
        """Display the main menu and handle user choices."""
        print("\n" + "="*40)
        print("🎯 NUMBER GUESSER")
        print("="*40)
        print("  1. Play Game")
        print("  2. View Stats")
        print("  3. Quit")
        print("="*40)
        
        while True:
            choice = input("\nWhat would you like to do? [1-3]: ").strip()
            
            if choice == '1':
                min_num, max_num = self.difficulty_menu()
                self.play_game(min_num, max_num)
                self.main_menu()
                break
            elif choice == '2':
                self.show_stats()
            elif choice == '3':
                print("\n👋 Thanks for playing! Come back soon!")
                if self.games_played > 0:
                    self.show_stats()
                sys.exit(0)
            else:
                print("Invalid choice! Pick 1-3.")

def main():
    """Entry point for the game."""
    print("\n" + "🎯" * 20)
    print("   Welcome to NUMBER GUESSER!")
    print("🎯" * 20)
    
    game = NumberGuesser()
    
    try:
        game.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted! Thanks for playing!")
        sys.exit(0)

if __name__ == "__main__":
    main()
