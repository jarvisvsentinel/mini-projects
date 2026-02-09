#!/usr/bin/env python3
"""
Regex Tester CLI - Test regular expressions with style!
A powerful CLI tool for testing regex patterns with colored output and match highlighting.
"""

import re
import sys
import argparse
from typing import List, Tuple, Optional

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'


def print_header(text: str):
    """Print a styled header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def highlight_matches(text: str, matches: List[Tuple[int, int]], color: str = Colors.BG_GREEN) -> str:
    """Highlight matches in text with background color."""
    if not matches:
        return text
    
    # Sort matches by start position
    matches = sorted(matches, key=lambda x: x[0])
    
    result = []
    last_end = 0
    
    for start, end in matches:
        # Add text before match
        result.append(text[last_end:start])
        # Add highlighted match
        result.append(f"{color}{Colors.BOLD}{text[start:end]}{Colors.RESET}")
        last_end = end
    
    # Add remaining text
    result.append(text[last_end:])
    
    return ''.join(result)


def test_regex(pattern: str, text: str, flags: int = 0) -> dict:
    """
    Test a regex pattern against text.
    
    Returns:
        dict with keys: success, matches, groups, error
    """
    try:
        compiled = re.compile(pattern, flags)
        matches = list(compiled.finditer(text))
        
        result = {
            'success': True,
            'match_count': len(matches),
            'matches': [],
            'groups': [],
            'spans': [],
            'error': None
        }
        
        for match in matches:
            result['matches'].append(match.group(0))
            result['spans'].append((match.start(), match.end()))
            
            # Capture groups
            groups = []
            for i, group in enumerate(match.groups(), 1):
                if group is not None:
                    groups.append({'index': i, 'value': group, 'span': match.span(i)})
            
            # Named groups
            for name, value in match.groupdict().items():
                if value is not None:
                    groups.append({'name': name, 'value': value})
            
            if groups:
                result['groups'].append(groups)
        
        return result
    
    except re.error as e:
        return {
            'success': False,
            'error': str(e),
            'match_count': 0,
            'matches': [],
            'groups': [],
            'spans': []
        }


def parse_flags(flag_string: str) -> int:
    """Parse flag string into regex flags."""
    flags = 0
    flag_map = {
        'i': re.IGNORECASE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'x': re.VERBOSE,
        'a': re.ASCII,
        'l': re.LOCALE
    }
    
    for char in flag_string.lower():
        if char in flag_map:
            flags |= flag_map[char]
    
    return flags


def interactive_mode():
    """Run in interactive mode."""
    print_header("REGEX TESTER - Interactive Mode")
    print_info("Enter 'quit' or 'exit' to quit")
    print_info("Use flags: i (ignorecase), m (multiline), s (dotall), x (verbose)")
    print()
    
    while True:
        try:
            # Get pattern
            pattern = input(f"{Colors.YELLOW}Pattern:{Colors.RESET} ").strip()
            if pattern.lower() in ['quit', 'exit', 'q']:
                print_info("Goodbye!")
                break
            
            if not pattern:
                continue
            
            # Get flags (optional)
            flags_str = input(f"{Colors.YELLOW}Flags (optional, e.g., 'im'):{Colors.RESET} ").strip()
            flags = parse_flags(flags_str) if flags_str else 0
            
            # Get test text
            print(f"{Colors.YELLOW}Text (press Enter twice to finish):{Colors.RESET}")
            lines = []
            while True:
                line = input()
                if line == '' and lines and lines[-1] == '':
                    lines.pop()  # Remove the last empty line
                    break
                lines.append(line)
            
            text = '\n'.join(lines)
            
            if not text:
                print_error("No text provided!")
                continue
            
            # Test the pattern
            result = test_regex(pattern, text, flags)
            
            print()
            if result['success']:
                if result['match_count'] > 0:
                    print_success(f"Found {result['match_count']} match(es)!")
                    
                    # Show highlighted text
                    print(f"\n{Colors.BOLD}Highlighted Text:{Colors.RESET}")
                    highlighted = highlight_matches(text, result['spans'])
                    print(highlighted)
                    
                    # Show matches
                    print(f"\n{Colors.BOLD}Matches:{Colors.RESET}")
                    for i, match in enumerate(result['matches'], 1):
                        print(f"  {Colors.CYAN}[{i}]{Colors.RESET} {repr(match)}")
                    
                    # Show groups if any
                    if result['groups']:
                        print(f"\n{Colors.BOLD}Capture Groups:{Colors.RESET}")
                        for i, groups in enumerate(result['groups'], 1):
                            print(f"  {Colors.CYAN}Match {i}:{Colors.RESET}")
                            for group in groups:
                                if 'name' in group:
                                    print(f"    {Colors.MAGENTA}(?P<{group['name']}>){Colors.RESET} = {repr(group['value'])}")
                                else:
                                    print(f"    {Colors.MAGENTA}Group {group['index']}{Colors.RESET} = {repr(group['value'])}")
                else:
                    print_error("No matches found!")
            else:
                print_error(f"Regex error: {result['error']}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n")
            print_info("Interrupted. Goodbye!")
            break
        except EOFError:
            print("\n")
            print_info("EOF. Goodbye!")
            break


def batch_mode(pattern: str, texts: List[str], flags: int = 0):
    """Run in batch mode with multiple test cases."""
    print_header(f"Testing Pattern: {pattern}")
    
    if flags:
        flag_names = []
        if flags & re.IGNORECASE: flag_names.append('IGNORECASE')
        if flags & re.MULTILINE: flag_names.append('MULTILINE')
        if flags & re.DOTALL: flag_names.append('DOTALL')
        if flags & re.VERBOSE: flag_names.append('VERBOSE')
        print_info(f"Flags: {', '.join(flag_names)}")
    
    print()
    
    for i, text in enumerate(texts, 1):
        print(f"{Colors.BOLD}Test Case {i}:{Colors.RESET}")
        print(f"Text: {repr(text)}")
        
        result = test_regex(pattern, text, flags)
        
        if result['success']:
            if result['match_count'] > 0:
                print_success(f"Matched! ({result['match_count']} match(es))")
                highlighted = highlight_matches(text, result['spans'])
                print(f"Result: {highlighted}")
                
                if result['matches']:
                    print(f"Matches: {', '.join(repr(m) for m in result['matches'])}")
            else:
                print_error("No match")
        else:
            print_error(f"Regex error: {result['error']}")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Regex Tester - Test regular expressions with style!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python regex_tester.py
  
  # Quick test
  python regex_tester.py -p "\\d+" -t "I have 42 apples"
  
  # With flags
  python regex_tester.py -p "hello" -t "HELLO world" -f i
  
  # Multiple test cases
  python regex_tester.py -p "\\w+" -t "hello" "world" "123"
  
  # Email validation
  python regex_tester.py -p "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" -t "test@example.com"
        """
    )
    
    parser.add_argument('-p', '--pattern', help='Regex pattern to test')
    parser.add_argument('-t', '--text', nargs='+', help='Text(s) to test against')
    parser.add_argument('-f', '--flags', default='', help='Regex flags (i=ignorecase, m=multiline, s=dotall, x=verbose)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Force interactive mode')
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or (not args.pattern and not args.text):
        interactive_mode()
    
    # Batch mode
    elif args.pattern and args.text:
        flags = parse_flags(args.flags)
        batch_mode(args.pattern, args.text, flags)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
