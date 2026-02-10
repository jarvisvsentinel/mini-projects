#!/usr/bin/env python3
"""
Password Manager CLI - Secure terminal-based password vault
Features: AES-256 encryption, password generation, clipboard integration, search
"""

import os
import sys
import json
import secrets
import string
import base64
import getpass
from pathlib import Path
from typing import Optional, Dict, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Constants
VAULT_DIR = Path.home() / ".password_vault"
VAULT_FILE = VAULT_DIR / "vault.enc"
SALT_FILE = VAULT_DIR / "salt.bin"


class PasswordVault:
    """Encrypted password storage with master password protection"""
    
    def __init__(self):
        self.vault_data: Dict[str, Dict] = {}
        self.cipher: Optional[Fernet] = None
        self._ensure_vault_dir()
    
    def _ensure_vault_dir(self):
        """Create vault directory if it doesn't exist"""
        VAULT_DIR.mkdir(exist_ok=True, mode=0o700)
    
    def _derive_key(self, master_password: str, salt: bytes) -> bytes:
        """Derive encryption key from master password using PBKDF2"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    def _get_or_create_salt(self) -> bytes:
        """Get existing salt or create new one"""
        if SALT_FILE.exists():
            return SALT_FILE.read_bytes()
        else:
            salt = os.urandom(16)
            SALT_FILE.write_bytes(salt)
            os.chmod(SALT_FILE, 0o600)
            return salt
    
    def initialize(self, master_password: str):
        """Initialize vault with master password"""
        salt = self._get_or_create_salt()
        key = self._derive_key(master_password, salt)
        self.cipher = Fernet(key)
        
        if VAULT_FILE.exists():
            try:
                encrypted_data = VAULT_FILE.read_bytes()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.vault_data = json.loads(decrypted_data.decode())
                return True
            except Exception:
                return False  # Invalid password
        else:
            self.vault_data = {}
            self._save_vault()
            return True
    
    def _save_vault(self):
        """Encrypt and save vault to disk"""
        if self.cipher is None:
            raise RuntimeError("Vault not initialized")
        
        json_data = json.dumps(self.vault_data, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        VAULT_FILE.write_bytes(encrypted_data)
        os.chmod(VAULT_FILE, 0o600)
    
    def add_entry(self, service: str, username: str, password: str, notes: str = ""):
        """Add new password entry"""
        self.vault_data[service.lower()] = {
            "service": service,
            "username": username,
            "password": password,
            "notes": notes
        }
        self._save_vault()
    
    def get_entry(self, service: str) -> Optional[Dict]:
        """Retrieve password entry"""
        return self.vault_data.get(service.lower())
    
    def delete_entry(self, service: str) -> bool:
        """Delete password entry"""
        if service.lower() in self.vault_data:
            del self.vault_data[service.lower()]
            self._save_vault()
            return True
        return False
    
    def search_entries(self, query: str) -> List[Dict]:
        """Search entries by service name or username"""
        query = query.lower()
        results = []
        for entry in self.vault_data.values():
            if query in entry["service"].lower() or query in entry["username"].lower():
                results.append(entry)
        return results
    
    def list_all(self) -> List[Dict]:
        """List all entries"""
        return list(self.vault_data.values())
    
    def update_entry(self, service: str, **kwargs):
        """Update existing entry"""
        if service.lower() in self.vault_data:
            entry = self.vault_data[service.lower()]
            for key, value in kwargs.items():
                if key in entry and value is not None:
                    entry[key] = value
            self._save_vault()
            return True
        return False


class PasswordGenerator:
    """Secure password generator"""
    
    @staticmethod
    def generate(length: int = 16, use_symbols: bool = True, use_numbers: bool = True) -> str:
        """Generate cryptographically secure random password"""
        chars = string.ascii_letters
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password
    
    @staticmethod
    def check_strength(password: str) -> tuple[str, int]:
        """Check password strength (score 0-100)"""
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 5
        
        # Character diversity
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        score += sum([has_lower, has_upper, has_digit, has_symbol]) * 15
        
        # Bonus for variety
        unique_chars = len(set(password))
        if unique_chars / length > 0.7:
            score += 20
        
        score = min(score, 100)
        
        if score >= 80:
            rating = "Strong"
        elif score >= 60:
            rating = "Good"
        elif score >= 40:
            rating = "Fair"
        else:
            rating = "Weak"
        
        return rating, score


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard if available"""
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    return False


def print_header():
    """Print application header"""
    print("\n" + "="*60)
    print("🔐  PASSWORD MANAGER CLI")
    print("="*60 + "\n")


def print_menu():
    """Print main menu"""
    print("\nOptions:")
    print("  1. Add new password")
    print("  2. Retrieve password")
    print("  3. List all entries")
    print("  4. Search entries")
    print("  5. Update entry")
    print("  6. Delete entry")
    print("  7. Generate password")
    print("  8. Change master password")
    print("  9. Exit")
    print()


def add_entry_interactive(vault: PasswordVault):
    """Interactive password entry addition"""
    print("\n--- Add New Password ---")
    service = input("Service name: ").strip()
    if not service:
        print("❌ Service name cannot be empty")
        return
    
    if vault.get_entry(service):
        print(f"⚠️  Entry for '{service}' already exists!")
        return
    
    username = input("Username/Email: ").strip()
    
    choice = input("Generate password? (y/n): ").strip().lower()
    if choice == 'y':
        length = input("Password length (default 16): ").strip()
        length = int(length) if length.isdigit() else 16
        password = PasswordGenerator.generate(length)
        print(f"\n🎲 Generated password: {password}")
        rating, score = PasswordGenerator.check_strength(password)
        print(f"💪 Strength: {rating} ({score}/100)")
    else:
        password = getpass.getpass("Password: ")
        if password:
            rating, score = PasswordGenerator.check_strength(password)
            print(f"💪 Strength: {rating} ({score}/100)")
    
    notes = input("Notes (optional): ").strip()
    
    vault.add_entry(service, username, password, notes)
    print(f"\n✅ Password for '{service}' added successfully!")


def retrieve_entry_interactive(vault: PasswordVault):
    """Interactive password retrieval"""
    print("\n--- Retrieve Password ---")
    service = input("Service name: ").strip()
    
    entry = vault.get_entry(service)
    if entry:
        print(f"\n📋 Service: {entry['service']}")
        print(f"👤 Username: {entry['username']}")
        print(f"🔑 Password: {entry['password']}")
        if entry.get('notes'):
            print(f"📝 Notes: {entry['notes']}")
        
        if copy_to_clipboard(entry['password']):
            print("\n✅ Password copied to clipboard!")
        else:
            print("\n⚠️  Clipboard not available (install pyperclip)")
    else:
        print(f"\n❌ No entry found for '{service}'")


def list_entries_interactive(vault: PasswordVault):
    """List all password entries"""
    entries = vault.list_all()
    
    if not entries:
        print("\n📭 No entries in vault")
        return
    
    print(f"\n--- All Entries ({len(entries)}) ---")
    entries.sort(key=lambda x: x['service'].lower())
    
    for entry in entries:
        print(f"\n🔹 {entry['service']}")
        print(f"   Username: {entry['username']}")
        if entry.get('notes'):
            print(f"   Notes: {entry['notes']}")


def search_entries_interactive(vault: PasswordVault):
    """Interactive entry search"""
    print("\n--- Search Entries ---")
    query = input("Search query: ").strip()
    
    if not query:
        print("❌ Search query cannot be empty")
        return
    
    results = vault.search_entries(query)
    
    if not results:
        print(f"\n❌ No entries found matching '{query}'")
        return
    
    print(f"\n--- Search Results ({len(results)}) ---")
    for entry in results:
        print(f"\n🔹 {entry['service']}")
        print(f"   Username: {entry['username']}")
        if entry.get('notes'):
            print(f"   Notes: {entry['notes']}")


def update_entry_interactive(vault: PasswordVault):
    """Interactive entry update"""
    print("\n--- Update Entry ---")
    service = input("Service name: ").strip()
    
    entry = vault.get_entry(service)
    if not entry:
        print(f"\n❌ No entry found for '{service}'")
        return
    
    print(f"\nCurrent values:")
    print(f"  Username: {entry['username']}")
    print(f"  Password: {entry['password']}")
    print(f"  Notes: {entry.get('notes', '')}")
    
    print("\nEnter new values (press Enter to keep current):")
    
    username = input("New username: ").strip()
    
    choice = input("Update password? (y/n): ").strip().lower()
    password = None
    if choice == 'y':
        gen_choice = input("Generate new password? (y/n): ").strip().lower()
        if gen_choice == 'y':
            length = input("Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            password = PasswordGenerator.generate(length)
            print(f"🎲 Generated password: {password}")
        else:
            password = getpass.getpass("New password: ")
    
    notes = input("New notes: ").strip()
    
    vault.update_entry(
        service,
        username=username or None,
        password=password,
        notes=notes or None
    )
    print(f"\n✅ Entry for '{service}' updated successfully!")


def delete_entry_interactive(vault: PasswordVault):
    """Interactive entry deletion"""
    print("\n--- Delete Entry ---")
    service = input("Service name: ").strip()
    
    entry = vault.get_entry(service)
    if not entry:
        print(f"\n❌ No entry found for '{service}'")
        return
    
    print(f"\n⚠️  About to delete entry for: {entry['service']}")
    confirm = input("Are you sure? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        vault.delete_entry(service)
        print(f"\n✅ Entry for '{service}' deleted")
    else:
        print("\n❌ Deletion cancelled")


def generate_password_interactive():
    """Interactive password generation"""
    print("\n--- Generate Password ---")
    
    length = input("Password length (default 16): ").strip()
    length = int(length) if length.isdigit() and int(length) > 0 else 16
    
    use_symbols = input("Include symbols? (y/n, default y): ").strip().lower() != 'n'
    use_numbers = input("Include numbers? (y/n, default y): ").strip().lower() != 'n'
    
    password = PasswordGenerator.generate(length, use_symbols, use_numbers)
    rating, score = PasswordGenerator.check_strength(password)
    
    print(f"\n🎲 Generated password: {password}")
    print(f"💪 Strength: {rating} ({score}/100)")
    
    if copy_to_clipboard(password):
        print("✅ Password copied to clipboard!")


def main():
    """Main application loop"""
    print_header()
    
    vault = PasswordVault()
    
    # Get master password
    if VAULT_FILE.exists():
        print("🔒 Vault exists. Enter master password to unlock.")
    else:
        print("🆕 Creating new vault. Set your master password.")
    
    while True:
        master_password = getpass.getpass("Master password: ")
        
        if vault.initialize(master_password):
            print("✅ Vault unlocked!\n")
            break
        else:
            print("❌ Invalid master password. Try again.\n")
    
    # Main loop
    while True:
        print_menu()
        choice = input("Select option (1-9): ").strip()
        
        if choice == '1':
            add_entry_interactive(vault)
        elif choice == '2':
            retrieve_entry_interactive(vault)
        elif choice == '3':
            list_entries_interactive(vault)
        elif choice == '4':
            search_entries_interactive(vault)
        elif choice == '5':
            update_entry_interactive(vault)
        elif choice == '6':
            delete_entry_interactive(vault)
        elif choice == '7':
            generate_password_interactive()
        elif choice == '8':
            print("\n⚠️  Master password change not yet implemented")
        elif choice == '9':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please select 1-9.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
