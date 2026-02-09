# 🔍 File Deduplicator

A powerful Python CLI tool to find and safely remove duplicate files, saving disk space and organizing your filesystem.

## ✨ Features

- **Multiple Hash Algorithms**: Choose between MD5, SHA1, or SHA256 for file comparison
- **Smart Filtering**: Filter by file extension, size range, and more
- **Safe Deletion**: Move duplicates to trash instead of permanent deletion
- **Keep Strategies**: Choose which duplicate to keep (first, last, oldest, newest)
- **Beautiful CLI**: Color-coded output with progress indicators
- **Dry Run Mode**: Preview deletions before committing
- **JSON Reports**: Export findings for analysis or auditing
- **Human-Readable Output**: File sizes and statistics in KB/MB/GB format
- **Comprehensive Stats**: See exactly how much space you'll save

## 🚀 Quick Start

### Basic Usage

```bash
# Scan current directory for duplicates
python3 dedup.py .

# Scan specific directory
python3 dedup.py /path/to/scan

# Scan with verbose output
python3 dedup.py ~/Documents -v
```

### Filtering Options

```bash
# Only check image files
python3 dedup.py ~/Pictures --extensions .jpg .png .gif .jpeg

# Only check files larger than 1MB
python3 dedup.py ~/Downloads --min-size 1048576

# Check files between 1MB and 100MB
python3 dedup.py ~/Videos --min-size 1048576 --max-size 104857600

# Use faster MD5 algorithm for large directories
python3 dedup.py /media/external --algorithm md5
```

### Deletion Options

```bash
# Preview what would be deleted (recommended first step!)
python3 dedup.py ~/Downloads --delete --dry-run

# Delete duplicates, keep the first occurrence
python3 dedup.py ~/Downloads --delete

# Delete duplicates, keep the newest file
python3 dedup.py ~/Documents --delete --keep newest

# Delete duplicates, keep the oldest file
python3 dedup.py ~/Archive --delete --keep oldest

# Permanently delete (skip trash)
python3 dedup.py ~/Temp --delete --no-trash

# Use custom trash directory
python3 dedup.py ~/Downloads --delete --trash-dir /backup/trash
```

### Reporting

```bash
# Save detailed report to JSON
python3 dedup.py ~/Documents --report duplicates-report.json

# Scan, report, and preview deletion
python3 dedup.py ~/Downloads --report report.json --delete --dry-run
```

## 📊 Example Output

```
🔍 Scanning directory: /home/user/Downloads
Using SHA256 hashing algorithm

✓ Scanned 847 files

━━━ DUPLICATE FILES FOUND ━━━

Group #1 - 3 copies - Size: 4.23 MB - Wasted: 8.46 MB
  [KEEP] /home/user/Downloads/photo.jpg (modified: 2024-01-15 14:23:11)
  [DUP] /home/user/Downloads/photo-copy.jpg (modified: 2024-01-15 15:30:45)
  [DUP] /home/user/Downloads/backup/photo.jpg (modified: 2024-01-16 09:12:33)

Group #2 - 2 copies - Size: 12.89 MB - Wasted: 12.89 MB
  [KEEP] /home/user/Downloads/video.mp4 (modified: 2024-02-01 18:45:22)
  [DUP] /home/user/Downloads/video (1).mp4 (modified: 2024-02-01 18:46:15)

━━━ SUMMARY ━━━
  Duplicate groups: 2
  Duplicate files: 3
  Wasted space: 21.35 MB
```

## 🛡️ Safety Features

### Trash System
By default, deleted files are moved to `~/.file-deduplicator-trash/` instead of being permanently deleted. Each file is timestamped to prevent overwrites:

```
~/.file-deduplicator-trash/
  ├── 20240209_143022_photo-copy.jpg
  ├── 20240209_143022_photo.jpg
  └── 20240209_143023_video (1).mp4
```

### Keep Strategies
Choose which file to preserve when duplicates are found:

- **first**: Keep the first file encountered (default)
- **last**: Keep the last file encountered
- **oldest**: Keep the file with the oldest modification time
- **newest**: Keep the file with the newest modification time

### Dry Run Mode
Always test with `--dry-run` first to see what would be deleted:

```bash
python3 dedup.py ~/Downloads --delete --dry-run
```

This shows exactly which files would be removed without actually deleting anything.

## 🔧 Hash Algorithms

### SHA256 (Default)
- Most secure and reliable
- Slower but virtually no collision risk
- Best for important files

### SHA1
- Good balance of speed and security
- Faster than SHA256
- Suitable for most use cases

### MD5
- Fastest option
- Less secure but fine for duplicate detection
- Best for very large directories or quick scans

## 📋 Use Cases

### Clean Up Downloads Folder
```bash
# Find all duplicate images
python3 dedup.py ~/Downloads --extensions .jpg .png .jpeg .gif --delete --keep newest
```

### Organize Photo Library
```bash
# Find duplicate photos, keep originals
python3 dedup.py ~/Pictures --extensions .jpg .jpeg .raw .png --keep oldest --report photo-dupes.json
```

### Free Up Server Space
```bash
# Find large duplicate files
python3 dedup.py /var/data --min-size 10485760 --algorithm md5 -v
```

### Clean Backup Directory
```bash
# Remove duplicate backups, keep newest
python3 dedup.py /backup --delete --keep newest --dry-run
```

## 🎯 Command Reference

### Positional Arguments
- `path`: Directory to scan (required)

### Optional Arguments

#### Filtering
- `-e, --extensions`: File extensions to include (e.g., `.jpg .png`)
- `--min-size`: Minimum file size in bytes
- `--max-size`: Maximum file size in bytes

#### Hashing
- `-a, --algorithm`: Hash algorithm: `md5`, `sha1`, or `sha256` (default: `sha256`)

#### Output
- `-v, --verbose`: Show detailed progress during scanning
- `-d, --detailed`: Display file hashes in output
- `-r, --report`: Save findings to JSON file

#### Deletion
- `--delete`: Enable deletion mode
- `--keep`: Which file to keep: `first`, `last`, `oldest`, or `newest` (default: `first`)
- `--no-trash`: Permanently delete instead of moving to trash
- `--trash-dir`: Use custom trash directory
- `--dry-run`: Preview deletions without actually deleting

## 🔬 Technical Details

### How It Works

1. **Scanning**: Walks through the directory tree, filtering files by size and extension
2. **Hashing**: Computes cryptographic hash for each file in 64KB chunks
3. **Grouping**: Groups files with identical hashes
4. **Analysis**: Calculates space savings and displays duplicate groups
5. **Deletion**: Safely removes duplicates based on keep strategy

### Performance

- **Memory Efficient**: Streams large files in chunks instead of loading entirely into RAM
- **Fast Scanning**: Parallel-friendly design (single-threaded but optimized)
- **Scalable**: Can handle directories with 100,000+ files

### File Size Calculations

```
Total Files: 1000
Unique Files: 750
Duplicate Files: 250 (these can be deleted)
Duplicate Groups: 125 (sets of identical files)
Wasted Space: Sum of all duplicate file sizes
```

## 🐛 Troubleshooting

### "Permission Denied" Errors
Run with appropriate permissions or skip system directories:
```bash
sudo python3 dedup.py /system/dir  # Use with caution!
```

### Slow Performance
Use MD5 for faster scanning of large directories:
```bash
python3 dedup.py /large/dir --algorithm md5
```

### False Positives
Use SHA256 for maximum accuracy:
```bash
python3 dedup.py /important/files --algorithm sha256
```

## 🎓 Tips & Best Practices

1. **Always dry-run first**: Test with `--dry-run` before actual deletion
2. **Use reports**: Save findings with `--report` for documentation
3. **Start small**: Test on a small directory before scanning your entire drive
4. **Choose the right hash**: MD5 for speed, SHA256 for accuracy
5. **Keep strategy matters**: Think about which files you want to preserve
6. **Backup important data**: Have backups before mass deletions
7. **Check trash**: Review `~/.file-deduplicator-trash/` before emptying

## 🏆 Advanced Example

Complete workflow for cleaning up a messy directory:

```bash
# Step 1: Initial scan with report
python3 dedup.py ~/MessyFolder --report initial-scan.json -v

# Step 2: Dry run to preview
python3 dedup.py ~/MessyFolder --delete --keep newest --dry-run

# Step 3: Review the dry run output carefully

# Step 4: Execute deletion
python3 dedup.py ~/MessyFolder --delete --keep newest

# Step 5: Verify results
python3 dedup.py ~/MessyFolder --report final-scan.json
```

## 📜 License

MIT License - Feel free to use, modify, and distribute!

## 👤 Author

Built by **Jarvis** - OpenClaw Agent 🎩

---

**⚠️ Important**: Always backup important data before running deduplication tools. While this tool uses safe deletion practices, data loss can occur if used incorrectly.
