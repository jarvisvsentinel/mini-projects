#!/usr/bin/env python3
"""
File Deduplicator - Find and remove duplicate files safely
Author: Jarvis (OpenClaw Agent)
"""

import os
import sys
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set
import shutil
import json
from datetime import datetime

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def format_bytes(size: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def hash_file(filepath: Path, algorithm: str = 'sha256', block_size: int = 65536) -> str:
    """
    Generate hash for a file using specified algorithm
    
    Args:
        filepath: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256)
        block_size: Size of blocks to read
        
    Returns:
        Hexadecimal hash string
    """
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    else:
        hasher = hashlib.sha256()
    
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except (IOError, PermissionError) as e:
        print(f"{Colors.YELLOW}⚠ Warning: Cannot read {filepath}: {e}{Colors.END}")
        return None

def scan_directory(
    path: Path,
    extensions: Set[str] = None,
    min_size: int = 0,
    max_size: int = None,
    algorithm: str = 'sha256',
    verbose: bool = False
) -> Dict[str, List[Path]]:
    """
    Scan directory for files and group by hash
    
    Args:
        path: Directory to scan
        extensions: Set of file extensions to include (None = all)
        min_size: Minimum file size in bytes
        max_size: Maximum file size in bytes
        algorithm: Hash algorithm to use
        verbose: Print progress messages
        
    Returns:
        Dictionary mapping file hashes to list of file paths
    """
    file_hashes = defaultdict(list)
    file_count = 0
    skipped_count = 0
    
    print(f"\n{Colors.CYAN}🔍 Scanning directory: {path}{Colors.END}")
    print(f"{Colors.BLUE}Using {algorithm.upper()} hashing algorithm{Colors.END}\n")
    
    for root, dirs, files in os.walk(path):
        for filename in files:
            filepath = Path(root) / filename
            
            # Skip symbolic links
            if filepath.is_symlink():
                continue
            
            try:
                file_size = filepath.stat().st_size
                
                # Apply size filters
                if file_size < min_size:
                    continue
                if max_size and file_size > max_size:
                    continue
                
                # Apply extension filter
                if extensions and filepath.suffix.lower() not in extensions:
                    skipped_count += 1
                    continue
                
                # Calculate hash
                file_hash = hash_file(filepath, algorithm)
                if file_hash:
                    file_hashes[file_hash].append(filepath)
                    file_count += 1
                    
                    if verbose and file_count % 100 == 0:
                        print(f"  Processed {file_count} files...", end='\r')
                        
            except (OSError, PermissionError) as e:
                if verbose:
                    print(f"{Colors.YELLOW}⚠ Skipping {filepath}: {e}{Colors.END}")
                continue
    
    if verbose:
        print(f"\n{Colors.GREEN}✓ Scanned {file_count} files{Colors.END}")
        if skipped_count > 0:
            print(f"{Colors.YELLOW}  Skipped {skipped_count} files (extension filter){Colors.END}")
    
    return file_hashes

def find_duplicates(file_hashes: Dict[str, List[Path]]) -> Dict[str, List[Path]]:
    """Filter hash dictionary to only include duplicates"""
    return {h: paths for h, paths in file_hashes.items() if len(paths) > 1}

def calculate_savings(duplicates: Dict[str, List[Path]]) -> tuple:
    """
    Calculate potential space savings from removing duplicates
    
    Returns:
        (total_duplicate_files, total_wasted_space)
    """
    total_files = 0
    total_space = 0
    
    for paths in duplicates.values():
        file_size = paths[0].stat().st_size
        # Keep one copy, count the rest as duplicates
        duplicate_count = len(paths) - 1
        total_files += duplicate_count
        total_space += file_size * duplicate_count
    
    return total_files, total_space

def display_duplicates(duplicates: Dict[str, List[Path]], detailed: bool = False):
    """Display duplicate files grouped by hash"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}━━━ DUPLICATE FILES FOUND ━━━{Colors.END}\n")
    
    group_num = 1
    for file_hash, paths in duplicates.items():
        file_size = paths[0].stat().st_size
        duplicate_count = len(paths) - 1
        wasted_space = file_size * duplicate_count
        
        print(f"{Colors.CYAN}Group #{group_num}{Colors.END} - "
              f"{Colors.YELLOW}{len(paths)} copies{Colors.END} - "
              f"Size: {Colors.GREEN}{format_bytes(file_size)}{Colors.END} - "
              f"Wasted: {Colors.RED}{format_bytes(wasted_space)}{Colors.END}")
        
        if detailed:
            print(f"  Hash: {file_hash[:16]}...")
        
        for i, path in enumerate(paths, 1):
            mod_time = datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            marker = f"{Colors.GREEN}[KEEP]{Colors.END}" if i == 1 else f"{Colors.RED}[DUP]{Colors.END}"
            print(f"  {marker} {path} (modified: {mod_time})")
        
        print()
        group_num += 1

def delete_duplicates(
    duplicates: Dict[str, List[Path]],
    keep_strategy: str = 'first',
    use_trash: bool = True,
    trash_dir: Path = None,
    dry_run: bool = False
) -> int:
    """
    Delete duplicate files, keeping one copy of each
    
    Args:
        duplicates: Dictionary of duplicate files
        keep_strategy: Which file to keep ('first', 'last', 'oldest', 'newest')
        use_trash: Move to trash instead of permanent deletion
        trash_dir: Custom trash directory path
        dry_run: Don't actually delete, just show what would be deleted
        
    Returns:
        Number of files deleted
    """
    if use_trash and trash_dir is None:
        trash_dir = Path.home() / '.file-deduplicator-trash'
        trash_dir.mkdir(exist_ok=True)
    
    deleted_count = 0
    
    for file_hash, paths in duplicates.items():
        # Determine which file to keep
        if keep_strategy == 'last':
            paths_sorted = paths[::-1]
        elif keep_strategy == 'oldest':
            paths_sorted = sorted(paths, key=lambda p: p.stat().st_mtime)
        elif keep_strategy == 'newest':
            paths_sorted = sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
        else:  # 'first'
            paths_sorted = paths
        
        # Keep the first one, delete the rest
        keep_file = paths_sorted[0]
        delete_files = paths_sorted[1:]
        
        for filepath in delete_files:
            try:
                if dry_run:
                    print(f"{Colors.YELLOW}[DRY RUN]{Colors.END} Would delete: {filepath}")
                    deleted_count += 1
                elif use_trash:
                    # Create trash subdirectory structure
                    trash_dest = trash_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filepath.name}"
                    shutil.move(str(filepath), str(trash_dest))
                    print(f"{Colors.GREEN}✓{Colors.END} Moved to trash: {filepath}")
                    deleted_count += 1
                else:
                    filepath.unlink()
                    print(f"{Colors.GREEN}✓{Colors.END} Deleted: {filepath}")
                    deleted_count += 1
            except Exception as e:
                print(f"{Colors.RED}✗ Error deleting {filepath}: {e}{Colors.END}")
    
    return deleted_count

def save_report(duplicates: Dict[str, List[Path]], output_file: Path):
    """Save duplicate files report to JSON"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_groups': len(duplicates),
        'duplicates': []
    }
    
    for file_hash, paths in duplicates.items():
        file_size = paths[0].stat().st_size
        report['duplicates'].append({
            'hash': file_hash,
            'size': file_size,
            'size_formatted': format_bytes(file_size),
            'count': len(paths),
            'files': [str(p) for p in paths]
        })
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"{Colors.GREEN}✓ Report saved to: {output_file}{Colors.END}")

def main():
    parser = argparse.ArgumentParser(
        description='Find and remove duplicate files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  %(prog)s .
  
  # Scan with size filter (files > 1MB)
  %(prog)s /path/to/scan --min-size 1048576
  
  # Only check image files
  %(prog)s /photos --extensions .jpg .png .gif
  
  # Delete duplicates (dry run first!)
  %(prog)s /path/to/scan --delete --dry-run
  
  # Delete duplicates, keep newest files
  %(prog)s /path/to/scan --delete --keep newest
  
  # Use MD5 for faster scanning
  %(prog)s /large/directory --algorithm md5
        """
    )
    
    parser.add_argument('path', type=str, help='Directory to scan')
    parser.add_argument('-e', '--extensions', nargs='+', help='File extensions to include (e.g., .jpg .png)')
    parser.add_argument('--min-size', type=int, default=0, help='Minimum file size in bytes')
    parser.add_argument('--max-size', type=int, help='Maximum file size in bytes')
    parser.add_argument('-a', '--algorithm', choices=['md5', 'sha1', 'sha256'], 
                       default='sha256', help='Hash algorithm (default: sha256)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-d', '--detailed', action='store_true', help='Show detailed information')
    parser.add_argument('--delete', action='store_true', help='Delete duplicate files')
    parser.add_argument('--keep', choices=['first', 'last', 'oldest', 'newest'],
                       default='first', help='Which duplicate to keep (default: first)')
    parser.add_argument('--no-trash', action='store_true', help='Permanently delete instead of moving to trash')
    parser.add_argument('--trash-dir', type=str, help='Custom trash directory')
    parser.add_argument('--dry-run', action='store_true', help="Show what would be deleted without deleting")
    parser.add_argument('-r', '--report', type=str, help='Save report to JSON file')
    
    args = parser.parse_args()
    
    # Validate path
    scan_path = Path(args.path)
    if not scan_path.exists():
        print(f"{Colors.RED}Error: Path does not exist: {scan_path}{Colors.END}")
        sys.exit(1)
    
    if not scan_path.is_dir():
        print(f"{Colors.RED}Error: Path is not a directory: {scan_path}{Colors.END}")
        sys.exit(1)
    
    # Prepare extensions filter
    extensions = None
    if args.extensions:
        extensions = {ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions}
        extensions = {ext.lower() for ext in extensions}
    
    # Scan directory
    file_hashes = scan_directory(
        scan_path,
        extensions=extensions,
        min_size=args.min_size,
        max_size=args.max_size,
        algorithm=args.algorithm,
        verbose=args.verbose
    )
    
    # Find duplicates
    duplicates = find_duplicates(file_hashes)
    
    if not duplicates:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ No duplicate files found!{Colors.END}")
        sys.exit(0)
    
    # Display results
    display_duplicates(duplicates, detailed=args.detailed)
    
    # Calculate savings
    duplicate_files, wasted_space = calculate_savings(duplicates)
    print(f"{Colors.HEADER}{Colors.BOLD}━━━ SUMMARY ━━━{Colors.END}")
    print(f"  Duplicate groups: {Colors.CYAN}{len(duplicates)}{Colors.END}")
    print(f"  Duplicate files: {Colors.YELLOW}{duplicate_files}{Colors.END}")
    print(f"  Wasted space: {Colors.RED}{format_bytes(wasted_space)}{Colors.END}\n")
    
    # Save report if requested
    if args.report:
        save_report(duplicates, Path(args.report))
    
    # Delete duplicates if requested
    if args.delete:
        if args.dry_run:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}DRY RUN MODE - No files will be deleted{Colors.END}\n")
        else:
            confirm = input(f"\n{Colors.RED}{Colors.BOLD}⚠ WARNING: About to delete {duplicate_files} files!{Colors.END}\nType 'yes' to confirm: ")
            if confirm.lower() != 'yes':
                print(f"{Colors.YELLOW}Deletion cancelled.{Colors.END}")
                sys.exit(0)
        
        trash_dir = Path(args.trash_dir) if args.trash_dir else None
        deleted = delete_duplicates(
            duplicates,
            keep_strategy=args.keep,
            use_trash=not args.no_trash,
            trash_dir=trash_dir,
            dry_run=args.dry_run
        )
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Processed {deleted} duplicate files{Colors.END}")
        if not args.no_trash and not args.dry_run:
            trash_location = trash_dir or (Path.home() / '.file-deduplicator-trash')
            print(f"{Colors.BLUE}Deleted files moved to: {trash_location}{Colors.END}")

if __name__ == '__main__':
    main()
