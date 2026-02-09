#!/usr/bin/env python3
"""
Flashcard App - A CLI-based spaced repetition learning tool
Study effectively with the SM-2 algorithm for optimal retention
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import argparse


class Card:
    """Represents a single flashcard with spaced repetition data"""
    
    def __init__(self, front: str, back: str, deck: str):
        self.front = front
        self.back = back
        self.deck = deck
        self.easiness = 2.5  # SM-2 algorithm default
        self.interval = 1  # Days until next review
        self.repetitions = 0
        self.next_review = datetime.now()
        self.created = datetime.now().isoformat()
        self.last_studied = None
        self.total_reviews = 0
        self.correct_reviews = 0
    
    def update_sm2(self, quality: int):
        """
        Update card using SM-2 spaced repetition algorithm
        quality: 0-5 (0=total blackout, 5=perfect response)
        """
        self.total_reviews += 1
        self.last_studied = datetime.now().isoformat()
        
        if quality >= 3:
            self.correct_reviews += 1
            
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.easiness)
            
            self.repetitions += 1
        else:
            self.repetitions = 0
            self.interval = 1
        
        # Update easiness factor
        self.easiness = max(1.3, self.easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Set next review date
        self.next_review = (datetime.now() + timedelta(days=self.interval)).isoformat()
    
    def is_due(self) -> bool:
        """Check if card is due for review"""
        return datetime.fromisoformat(self.next_review) <= datetime.now()
    
    def to_dict(self) -> dict:
        """Convert card to dictionary for JSON storage"""
        return {
            'front': self.front,
            'back': self.back,
            'deck': self.deck,
            'easiness': self.easiness,
            'interval': self.interval,
            'repetitions': self.repetitions,
            'next_review': self.next_review if isinstance(self.next_review, str) else self.next_review.isoformat(),
            'created': self.created,
            'last_studied': self.last_studied,
            'total_reviews': self.total_reviews,
            'correct_reviews': self.correct_reviews
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Card':
        """Create card from dictionary"""
        card = cls(data['front'], data['back'], data['deck'])
        card.easiness = data.get('easiness', 2.5)
        card.interval = data.get('interval', 1)
        card.repetitions = data.get('repetitions', 0)
        card.next_review = data.get('next_review', datetime.now().isoformat())
        card.created = data.get('created', datetime.now().isoformat())
        card.last_studied = data.get('last_studied')
        card.total_reviews = data.get('total_reviews', 0)
        card.correct_reviews = data.get('correct_reviews', 0)
        return card


class FlashcardApp:
    """Main application for managing flashcard decks and studying"""
    
    def __init__(self, data_file: str = "flashcards.json"):
        self.data_file = Path(data_file)
        self.cards: List[Card] = []
        self.load_cards()
    
    def load_cards(self):
        """Load cards from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.cards = [Card.from_dict(card_data) for card_data in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️  Error loading cards: {e}")
                self.cards = []
        else:
            self.cards = []
    
    def save_cards(self):
        """Save cards to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump([card.to_dict() for card in self.cards], f, indent=2)
    
    def add_card(self, front: str, back: str, deck: str = "default"):
        """Add a new flashcard"""
        card = Card(front, back, deck)
        self.cards.append(card)
        self.save_cards()
        print(f"✅ Card added to deck '{deck}'")
    
    def list_decks(self) -> Dict[str, int]:
        """Get all decks with card counts"""
        decks = {}
        for card in self.cards:
            decks[card.deck] = decks.get(card.deck, 0) + 1
        return decks
    
    def get_due_cards(self, deck: Optional[str] = None) -> List[Card]:
        """Get cards that are due for review"""
        cards = [c for c in self.cards if c.is_due()]
        if deck:
            cards = [c for c in cards if c.deck == deck]
        return cards
    
    def study_session(self, deck: Optional[str] = None, limit: int = 20):
        """Start a study session"""
        due_cards = self.get_due_cards(deck)
        
        if not due_cards:
            print("🎉 No cards due for review! Come back later.")
            return
        
        # Limit number of cards
        study_cards = random.sample(due_cards, min(len(due_cards), limit))
        
        print(f"\n📚 Study Session")
        print(f"Cards to review: {len(study_cards)}")
        if deck:
            print(f"Deck: {deck}")
        print("-" * 50)
        
        correct = 0
        total = len(study_cards)
        
        for i, card in enumerate(study_cards, 1):
            print(f"\n[{i}/{total}]")
            print(f"Q: {card.front}")
            input("Press Enter to reveal answer...")
            print(f"A: {card.back}")
            
            print("\nHow well did you know it?")
            print("0 = Total blackout")
            print("1 = Incorrect, but familiar")
            print("2 = Incorrect, but almost")
            print("3 = Correct, but difficult")
            print("4 = Correct, with hesitation")
            print("5 = Perfect!")
            
            while True:
                try:
                    rating = int(input("Rating (0-5): "))
                    if 0 <= rating <= 5:
                        break
                    print("Please enter a number between 0 and 5")
                except ValueError:
                    print("Please enter a valid number")
            
            card.update_sm2(rating)
            if rating >= 3:
                correct += 1
        
        self.save_cards()
        
        # Session summary
        print("\n" + "="*50)
        print("📊 Session Complete!")
        print(f"Score: {correct}/{total} ({(correct/total*100):.1f}%)")
        print("="*50)
    
    def stats(self, deck: Optional[str] = None):
        """Display statistics"""
        cards = self.cards if not deck else [c for c in self.cards if c.deck == deck]
        
        if not cards:
            print("No cards found")
            return
        
        total = len(cards)
        due = len([c for c in cards if c.is_due()])
        studied = len([c for c in cards if c.total_reviews > 0])
        
        total_reviews = sum(c.total_reviews for c in cards)
        correct_reviews = sum(c.correct_reviews for c in cards)
        accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
        
        print("\n📊 Statistics")
        if deck:
            print(f"Deck: {deck}")
        print("-" * 50)
        print(f"Total cards: {total}")
        print(f"Cards studied: {studied}")
        print(f"Cards due: {due}")
        print(f"Total reviews: {total_reviews}")
        print(f"Accuracy: {accuracy:.1f}%")
        print("-" * 50)
    
    def list_cards(self, deck: Optional[str] = None):
        """List all cards"""
        cards = self.cards if not deck else [c for c in self.cards if c.deck == deck]
        
        if not cards:
            print("No cards found")
            return
        
        print(f"\n📇 Cards ({len(cards)} total)")
        if deck:
            print(f"Deck: {deck}")
        print("-" * 50)
        
        for i, card in enumerate(cards, 1):
            due_str = "✅ Due" if card.is_due() else f"📅 Due {card.next_review[:10]}"
            print(f"{i}. {card.front[:40]}... | {due_str}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Flashcard App - Spaced repetition learning tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flashcard.py add "What is Python?" "A programming language"
  flashcard.py add "Capital of France" "Paris" --deck geography
  flashcard.py study
  flashcard.py study --deck geography --limit 10
  flashcard.py stats
  flashcard.py list
        """
    )
    
    parser.add_argument('command', choices=['add', 'study', 'stats', 'list', 'decks'],
                       help='Command to execute')
    parser.add_argument('front', nargs='?', help='Front of card (for add)')
    parser.add_argument('back', nargs='?', help='Back of card (for add)')
    parser.add_argument('--deck', '-d', default='default', help='Deck name')
    parser.add_argument('--limit', '-l', type=int, default=20, help='Max cards per study session')
    parser.add_argument('--file', '-f', default='flashcards.json', help='Data file location')
    
    args = parser.parse_args()
    
    app = FlashcardApp(args.file)
    
    if args.command == 'add':
        if not args.front or not args.back:
            print("❌ Error: Please provide both front and back of card")
            parser.print_help()
            return
        app.add_card(args.front, args.back, args.deck)
    
    elif args.command == 'study':
        deck = None if args.deck == 'default' else args.deck
        app.study_session(deck, args.limit)
    
    elif args.command == 'stats':
        deck = None if args.deck == 'default' else args.deck
        app.stats(deck)
    
    elif args.command == 'list':
        deck = None if args.deck == 'default' else args.deck
        app.list_cards(deck)
    
    elif args.command == 'decks':
        decks = app.list_decks()
        print("\n📚 Decks")
        print("-" * 50)
        for deck, count in sorted(decks.items()):
            print(f"{deck}: {count} cards")


if __name__ == "__main__":
    main()
