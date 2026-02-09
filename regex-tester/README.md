# 🔍 Regex Tester CLI

A powerful, user-friendly command-line tool for testing regular expressions with colored output, match highlighting, and capture group visualization.

## ✨ Features

- **🎨 Colored Output**: Beautiful syntax highlighting for matches and groups
- **🔦 Match Highlighting**: Visual highlighting of matched text with background colors
- **📦 Capture Groups**: Clear display of capture groups (numbered and named)
- **🚩 Flag Support**: Support for all standard regex flags (IGNORECASE, MULTILINE, DOTALL, VERBOSE, etc.)
- **💬 Interactive Mode**: Test patterns interactively with multi-line input
- **⚡ Batch Mode**: Test one pattern against multiple test cases
- **❌ Error Handling**: Clear error messages for invalid regex patterns
- **🎯 Multiple Matches**: Shows all matches, not just the first one

## 🚀 Installation

No installation required! Just make the script executable:

```bash
chmod +x regex_tester.py
```

## 📖 Usage

### Interactive Mode (Default)

Launch the interactive tester - great for experimenting with patterns:

```bash
python regex_tester.py
# or
./regex_tester.py -i
```

**Interactive Mode Features:**
- Enter your regex pattern
- Optionally specify flags (i, m, s, x, a, l)
- Enter multi-line text (press Enter twice to finish)
- See highlighted matches and capture groups
- Type 'quit' or 'exit' to quit

### Quick Test Mode

Test a pattern against text directly from the command line:

```bash
# Basic test
python regex_tester.py -p "\d+" -t "I have 42 apples and 13 oranges"

# Case-insensitive test
python regex_tester.py -p "hello" -t "HELLO world" -f i

# Multiple test cases
python regex_tester.py -p "\w+" -t "hello" "world" "test123"
```

### Examples

#### 1. Email Validation
```bash
python regex_tester.py -p "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" -t "test@example.com" "invalid@" "user@domain.co.uk"
```

#### 2. Phone Number Extraction
```bash
python regex_tester.py -p "\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}" -t "Call me at (555) 123-4567 or 555.987.6543"
```

#### 3. URL Matching
```bash
python regex_tester.py -p "https?://[^\s]+" -t "Visit https://example.com and http://test.org"
```

#### 4. Named Capture Groups
```bash
python regex_tester.py -p "(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})" -t "Today is 2026-02-09"
```

#### 5. Case-Insensitive Word Boundary
```bash
python regex_tester.py -p "\bpython\b" -t "I love Python programming" -f i
```

#### 6. Multi-line Text Matching
```bash
python regex_tester.py -p "^ERROR.*$" -t "INFO: Starting\nERROR: Failed\nWARNING: Check this" -f m
```

## 🚩 Regex Flags

Specify flags using the `-f` option. Multiple flags can be combined:

- **i** - IGNORECASE: Case-insensitive matching
- **m** - MULTILINE: ^ and $ match line boundaries
- **s** - DOTALL: . matches newlines
- **x** - VERBOSE: Ignore whitespace and allow comments
- **a** - ASCII: Make \w, \W, \b, etc. ASCII-only
- **l** - LOCALE: Make \w, \W, \b, etc. locale-dependent

**Example:**
```bash
python regex_tester.py -p "hello" -t "HELLO\nworld" -f im
```

## 🎨 Output Colors

The tool uses ANSI colors to make output more readable:

- 🟢 **Green Background**: Matched text
- 🟦 **Blue**: Informational messages
- ✅ **Green Text**: Success messages
- ❌ **Red Text**: Error messages
- 🟣 **Magenta**: Capture group labels
- 🔵 **Cyan**: Match indices and headers

## 📋 Command Line Options

```
usage: regex_tester.py [-h] [-p PATTERN] [-t TEXT [TEXT ...]] [-f FLAGS] [-i]

Regex Tester - Test regular expressions with style!

optional arguments:
  -h, --help            show this help message and exit
  -p, --pattern PATTERN
                        Regex pattern to test
  -t, --text TEXT [TEXT ...]
                        Text(s) to test against
  -f, --flags FLAGS     Regex flags (i=ignorecase, m=multiline, s=dotall, x=verbose)
  -i, --interactive     Force interactive mode
```

## 💡 Tips & Tricks

1. **Escape Special Characters**: Remember to escape backslashes in shell:
   - Use `"\d+"` instead of `\d+`
   - Or use single quotes: `'\d+'`

2. **Multi-line Input**: In interactive mode, press Enter twice to submit text

3. **Quick Exit**: Press Ctrl+C or type 'quit' to exit interactive mode

4. **Testing Edge Cases**: Use batch mode to test multiple cases at once

5. **Named Groups**: Use `(?P<name>...)` for named capture groups - they're displayed with their names!

## 🧪 Common Use Cases

### Data Extraction
Extract structured data from text (emails, phone numbers, dates, URLs)

### Input Validation
Test if user input matches expected patterns (forms, APIs)

### Log Analysis
Parse and filter log files with complex patterns

### Text Processing
Find and highlight patterns in documents

### Learning Regex
Experiment and learn regex in an interactive environment

## 🎯 Advanced Examples

### Extract Hashtags from Social Media Text
```bash
python regex_tester.py -p "#\w+" -t "Love #Python and #Regex! #CLI tools are awesome"
```

### Parse CSV-like Data
```bash
python regex_tester.py -p '(?P<name>[^,]+),(?P<age>\d+),(?P<city>[^,]+)' -t "John,30,NYC" "Jane,25,LA"
```

### Find IPv4 Addresses
```bash
python regex_tester.py -p "\b(?:\d{1,3}\.){3}\d{1,3}\b" -t "Server at 192.168.1.1 and 10.0.0.5"
```

### Match Markdown Headers
```bash
python regex_tester.py -p "^#+\s+.+$" -t "# Title\n## Section\nNot a header" -f m
```

## 🐛 Error Handling

The tool provides clear error messages for common regex issues:

- Invalid regex syntax
- Unmatched parentheses
- Invalid escape sequences
- Invalid backreferences

Example:
```bash
python regex_tester.py -p "(" -t "test"
# Output: ✗ Regex error: missing ), unterminated subpattern at position 0
```

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this tool!

## 📄 License

MIT License - Free to use and modify!

## 🎓 Learning Resources

- [Python Regex Documentation](https://docs.python.org/3/library/re.html)
- [Regex101](https://regex101.com/) - Online regex tester
- [RegexOne](https://regexone.com/) - Interactive regex tutorial

---

**Built with ❤️ by Jarvis** | Part of the Mini Projects Collection
