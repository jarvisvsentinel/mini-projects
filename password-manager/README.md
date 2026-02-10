# 🔐 Password Manager CLI

A secure, terminal-based password vault with military-grade encryption, password generation, and clipboard integration.

## Features

- **🛡️ AES-256 Encryption**: Your passwords are protected with industry-standard encryption
- **🔑 Master Password**: Single password protects your entire vault
- **🎲 Password Generator**: Create cryptographically secure random passwords
- **💪 Strength Checker**: Real-time password strength analysis
- **📋 Clipboard Integration**: Automatically copy passwords to clipboard
- **🔍 Search**: Find entries by service name or username
- **📝 Notes**: Store additional information with each entry
- **🔒 Secure Storage**: Vault stored in `~/.password_vault/` with restricted permissions

## Installation

### Requirements

- Python 3.8+
- `cryptography` library
- `pyperclip` library (optional, for clipboard support)

### Setup

```bash
# Install dependencies
pip install cryptography pyperclip

# Make executable
chmod +x password_manager.py

# Run
./password_manager.py
```

## Usage

### First Run

On first launch, you'll be prompted to create a master password:

```
🆕 Creating new vault. Set your master password.
Master password: ********
✅ Vault unlocked!
```

**⚠️ IMPORTANT**: Don't forget your master password! There's no recovery option.

### Main Menu

```
Options:
  1. Add new password
  2. Retrieve password
  3. List all entries
  4. Search entries
  5. Update entry
  6. Delete entry
  7. Generate password
  8. Change master password
  9. Exit
```

### Adding a Password

```
--- Add New Password ---
Service name: GitHub
Username/Email: shayn@example.com
Generate password? (y/n): y
Password length (default 16): 20

🎲 Generated password: k#7mL@9pR$2nX&5qT^8w
💪 Strength: Strong (100/100)
Notes (optional): Personal account

✅ Password for 'GitHub' added successfully!
```

### Retrieving a Password

```
--- Retrieve Password ---
Service name: GitHub

📋 Service: GitHub
👤 Username: shayn@example.com
🔑 Password: k#7mL@9pR$2nX&5qT^8w
📝 Notes: Personal account

✅ Password copied to clipboard!
```

### Generating Passwords

The password generator creates cryptographically secure passwords using Python's `secrets` module:

```
--- Generate Password ---
Password length (default 16): 24
Include symbols? (y/n, default y): y
Include numbers? (y/n, default y): y

🎲 Generated password: 3k$L9#mP@7nX&2qR^5wT*8zY
💪 Strength: Strong (100/100)
✅ Password copied to clipboard!
```

### Password Strength Ratings

The built-in strength checker evaluates passwords based on:
- **Length** (6-12+ characters)
- **Character diversity** (lowercase, uppercase, numbers, symbols)
- **Uniqueness** (ratio of unique characters)

Ratings:
- **Strong**: 80-100 points ✅
- **Good**: 60-79 points 👍
- **Fair**: 40-59 points ⚠️
- **Weak**: 0-39 points ❌

## Security Features

### Encryption

- **Algorithm**: AES-256 via Fernet (symmetric encryption)
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt**: Unique 16-byte random salt per vault
- **Encoding**: Base64 for safe storage

### File Permissions

All vault files are automatically secured:
- Vault file: `0600` (owner read/write only)
- Salt file: `0600` (owner read/write only)
- Vault directory: `0700` (owner access only)

### Password Generation

- Uses `secrets` module (cryptographically strong random)
- Not based on `random` (which is predictable)
- Customizable length and character sets

## File Structure

```
~/.password_vault/
├── vault.enc        # Encrypted password database
└── salt.bin         # Encryption salt (unique per vault)
```

## Examples

### Secure Your Vault

```bash
# The vault is automatically encrypted
# Each time you run the app, you'll need your master password

./password_manager.py
Master password: ********
```

### Quick Password Generation

Generate a 32-character password with all character types:

```bash
# In the app menu, select option 7
7
Password length (default 16): 32
Include symbols? (y/n, default y): y
Include numbers? (y/n, default y): y
```

### Search Across Entries

Find all entries related to "google":

```bash
# In the app menu, select option 4
4
Search query: google

--- Search Results (3) ---
🔹 Google Drive
   Username: shayn@gmail.com
🔹 Google Cloud
   Username: admin@example.com
🔹 Gmail
   Username: shayn@gmail.com
```

## Best Practices

1. **Master Password**: Use a strong, memorable passphrase (20+ characters recommended)
2. **Backups**: Regularly backup `~/.password_vault/` to a secure location
3. **Generated Passwords**: Use 16+ character passwords for maximum security
4. **Unique Passwords**: Never reuse passwords across services
5. **Regular Updates**: Change passwords periodically, especially for sensitive accounts

## Troubleshooting

### "Clipboard not available" Warning

Install pyperclip for clipboard support:
```bash
pip install pyperclip
```

### "Invalid master password"

Your master password is incorrect. There's no recovery option - you must remember it.

### Permission Denied

The vault files have restricted permissions. Make sure you're the owner:
```bash
ls -la ~/.password_vault/
# Should show: -rw------- (600)
```

## Limitations

- Master password cannot be changed (yet)
- No cloud sync
- No biometric unlock
- No browser integration
- No shared vaults

## Security Disclaimer

This is a demonstration project. For production use, consider established password managers like:
- Bitwarden
- 1Password
- KeePassXC

However, this tool uses proper cryptographic practices and is suitable for personal use.

## License

MIT License - Do whatever you want with it!

## Future Enhancements

- [ ] Master password change functionality
- [ ] Import/export (encrypted)
- [ ] Two-factor authentication
- [ ] Password expiration reminders
- [ ] Breach checking (HIBP API)
- [ ] Secure file attachments
- [ ] Multiple vaults
- [ ] Password history

---

**Built by Jarvis** 🎩 | Part of the Mini Projects Collection
