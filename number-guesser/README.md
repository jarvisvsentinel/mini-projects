# 🎯 Number Guesser

A fun, interactive number guessing game with personality and stats tracking!

## 🎮 Features

- **Multiple Difficulty Levels**: Choose from Easy (1-50), Medium (1-100), Hard (1-500), or Insane (1-1000)
- **Smart Hints**: Get contextual feedback on how close you are to the target
- **Stats Tracking**: Track your games played, total guesses, average performance, and personal best
- **Personality**: Celebratory messages and emojis make the game engaging
- **Clean Interface**: Simple menu system with intuitive controls

## 📋 Requirements

- Python 3.6 or higher (uses f-strings)
- No external dependencies - pure Python!

## 🚀 Usage

Run the game:
```bash
python3 game.py
# or
./game.py
```

### Main Menu
- **1. Play Game**: Start a new game and choose your difficulty
- **2. View Stats**: See your performance statistics
- **3. Quit**: Exit the game (shows final stats if you played)

### Gameplay
- Enter a number within the chosen range
- Get feedback on whether your guess is too high or too low
- Hints get more specific as you get closer to the target
- Type 'quit' during a game to give up and reveal the answer

## 🏆 Scoring

- **1 guess**: LEGENDARY! Are you psychic?!
- **2-3 guesses**: Incredible! You're a natural!
- **4-7 guesses**: Nice work! Solid performance!
- **8-15 guesses**: Not bad! Keep practicing!
- **16+ guesses**: You got there eventually!

## 🎯 Strategy Tips

1. Start with the middle of the range
2. Use binary search for optimal guessing
3. Pay attention to the hint intensity ("Way too high" vs "Close!")
4. Easy mode is perfect for learning the strategy

## 📊 Stats Tracked

- **Games Played**: Total number of completed games
- **Total Guesses**: Cumulative guesses across all games
- **Average Guesses**: Your typical performance
- **Best Score**: Your lowest number of guesses in a single game

## 🎨 Example Session

```
🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯
   Welcome to NUMBER GUESSER!
🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯

========================================
🎯 NUMBER GUESSER
========================================
  1. Play Game
  2. View Stats
  3. Quit
========================================

What would you like to do? [1-3]: 1

🎮 Choose your difficulty:
  1. Easy (1-50)
  2. Medium (1-100)
  3. Hard (1-500)
  4. Insane (1-1000)

Difficulty [1-4]: 2

🎯 I'm thinking of a number between 1 and 100...
Can you guess it? (Type 'quit' to exit)

Your guess: 50
📈 Too high! You're in the zone...
Your guess: 25
📉 Too low! Getting warmer though...
Your guess: 37
📈 So close! Just a tad lower!
Your guess: 35

🎉 CORRECT! You got it in 4 guesses!
🏆 NEW PERSONAL BEST!
🔥 Incredible! You're a natural!
```

## 🛠️ Technical Details

- Pure Python implementation (no dependencies)
- Object-oriented design with the `NumberGuesser` class
- Handles edge cases (invalid input, out-of-range guesses, keyboard interrupts)
- Persistent stats within a session (resets when you restart the program)

## 📝 License

Built with 💚 by Jarvis for the Mini Projects collection.

## 🚀 Future Enhancements

Potential features for future versions:
- Persistent stats saved to a JSON file
- Leaderboard with timestamps
- Multiplayer mode (two-player guessing competition)
- Hints system (limited hints per game)
- Timed mode for extra challenge

---

**Built**: February 8, 2026  
**Part of**: Sentinel Research Partners Mini Projects Collection
