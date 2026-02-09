# 📚 Flashcard App

A powerful CLI-based spaced repetition learning tool implementing the SM-2 algorithm for optimal retention and efficient studying.

## Features

- **Spaced Repetition (SM-2 Algorithm)**: Cards are scheduled for review at optimal intervals based on your performance
- **Multiple Decks**: Organize cards by topic (languages, science, history, etc.)
- **Progress Tracking**: Monitor your learning with detailed statistics
- **Smart Scheduling**: Cards appear when you're most likely to forget them
- **Easy Management**: Add, study, and track cards with simple commands
- **Persistent Storage**: All data saved in JSON format

## Installation

```bash
chmod +x flashcard.py
```

## Usage

### Add Cards

```bash
# Add to default deck
./flashcard.py add "What is Python?" "A programming language"

# Add to specific deck
./flashcard.py add "Capital of France" "Paris" --deck geography
./flashcard.py add "Hola" "Hello" --deck spanish
```

### Study Session

```bash
# Study all due cards (max 20)
./flashcard.py study

# Study specific deck
./flashcard.py study --deck geography

# Study with custom limit
./flashcard.py study --limit 50
```

During study, rate each card 0-5:
- **0** = Total blackout (complete guess)
- **1** = Incorrect, but familiar
- **2** = Incorrect, but almost got it
- **3** = Correct, but difficult
- **4** = Correct, with some hesitation
- **5** = Perfect recall!

### View Statistics

```bash
# Stats for all cards
./flashcard.py stats

# Stats for specific deck
./flashcard.py stats --deck spanish
```

### List Cards

```bash
# List all cards
./flashcard.py list

# List cards in specific deck
./flashcard.py list --deck geography
```

### View Decks

```bash
./flashcard.py decks
```

## How Spaced Repetition Works

The app uses the **SM-2 algorithm** (SuperMemo 2):

1. **New cards** appear the next day
2. **Easy cards** (rated 4-5) have intervals that grow exponentially
3. **Difficult cards** (rated 0-2) reset to 1 day
4. Each card has an "easiness factor" that adjusts based on your performance

This ensures you review:
- New/difficult material frequently
- Well-known material infrequently
- Everything right before you're about to forget it

## Examples

### Learning Spanish

```bash
# Add vocabulary
./flashcard.py add "Perro" "Dog" --deck spanish
./flashcard.py add "Gato" "Cat" --deck spanish
./flashcard.py add "Buenos días" "Good morning" --deck spanish

# Study
./flashcard.py study --deck spanish

# Check progress
./flashcard.py stats --deck spanish
```

### Medical School

```bash
# Add anatomy facts
./flashcard.py add "Largest bone in human body" "Femur" --deck anatomy
./flashcard.py add "Normal resting heart rate" "60-100 bpm" --deck physiology

# Study mixed
./flashcard.py study --limit 100
```

### Programming Concepts

```bash
./flashcard.py add "Time complexity of binary search" "O(log n)" --deck algorithms
./flashcard.py add "Python list vs tuple" "List is mutable, tuple is immutable" --deck python
```

## Data Storage

Cards are stored in `flashcards.json` by default. You can use a different file:

```bash
./flashcard.py add "Question" "Answer" --file my_cards.json
./flashcard.py study --file my_cards.json
```

## Tips for Effective Learning

1. **Study daily**: Even 10 minutes per day is more effective than cramming
2. **Be honest with ratings**: Don't rate cards easy if you struggled
3. **Use multiple decks**: Separate topics for focused study sessions
4. **Add context**: Make card backs detailed enough to understand
5. **Review consistently**: The algorithm works best with regular use

## Advanced Features

### Card Scheduling

Each card tracks:
- **Easiness factor**: How easy you find this card (1.3-2.5)
- **Interval**: Days until next review
- **Repetitions**: Consecutive correct reviews
- **Next review date**: When card becomes due

### Statistics Tracked

- Total cards and cards studied
- Cards currently due for review
- Total reviews performed
- Overall accuracy percentage
- Per-deck breakdowns

## Why Use This?

- **Proven method**: SM-2 has been used successfully since 1988
- **Efficient**: Learn more in less time
- **Offline**: No internet required, your data stays local
- **Simple**: Pure Python with zero dependencies
- **Flexible**: Works for any memorization task

## Requirements

- Python 3.6+
- No external dependencies!

## License

MIT License - Learn away! 🚀
