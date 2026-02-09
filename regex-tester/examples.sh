#!/bin/bash
# Example commands for the Regex Tester CLI

echo "=== Regex Tester Examples ==="
echo ""

echo "1. Email Validation"
python3 regex_tester.py -p "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" \
  -t "test@example.com" "invalid.email" "user@domain.co.uk"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "2. Phone Number Extraction"
python3 regex_tester.py -p "\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}" \
  -t "Call me at (555) 123-4567 or 555.987.6543"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "3. Extract Hashtags"
python3 regex_tester.py -p "#\w+" \
  -t "Love #Python and #Regex! #CLI tools are awesome"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "4. Date Parsing with Named Groups"
python3 regex_tester.py -p "(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})" \
  -t "Today is 2026-02-09 and tomorrow is 2026-02-10"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "5. Case-Insensitive Matching"
python3 regex_tester.py -p "\bpython\b" \
  -t "I love Python programming and PYTHON is great" -f i
echo ""
read -p "Press Enter to continue..."
echo ""

echo "6. URL Extraction"
python3 regex_tester.py -p "https?://[^\s]+" \
  -t "Visit https://example.com and http://test.org for more info"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "7. IPv4 Address Matching"
python3 regex_tester.py -p "\b(?:\d{1,3}\.){3}\d{1,3}\b" \
  -t "Server at 192.168.1.1 and 10.0.0.5 are online"
echo ""

echo "=== Examples Complete! ==="
echo "Try interactive mode: python3 regex_tester.py"
