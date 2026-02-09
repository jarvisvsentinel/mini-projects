# 📝 Markdown Live Previewer

A beautiful, feature-rich web-based markdown editor with live preview. Write markdown on the left, see the rendered result on the right - in real-time!

![Markdown Previewer](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0-green.svg)

## ✨ Features

### 🎯 Core Features
- **Live Preview**: See your markdown rendered in real-time as you type
- **Split View**: Side-by-side editor and preview panes
- **GitHub Flavored Markdown**: Full GFM support including tables, task lists, and strikethrough
- **Syntax Highlighting**: Beautiful code syntax highlighting powered by Highlight.js
- **File Operations**: Save and load `.md` files directly from the app
- **Dark/Light Theme**: Toggle between dark and light themes
- **Keyboard Shortcuts**: Quick access to common operations

### 📊 Statistics
- Live word count
- Character count
- Line count

### 🎨 UI/UX
- Clean, modern interface
- Responsive design (works on mobile!)
- Smooth animations and transitions
- Toast notifications for user feedback
- Modal dialogs for file operations

### ⌨️ Keyboard Shortcuts
- `Ctrl/Cmd + S` - Save file
- `Ctrl/Cmd + O` - Open file

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

#### Option 1: Quick Start (Recommended)
```bash
cd markdown-previewer
./run.sh
```

The script will automatically:
- Create a virtual environment if needed
- Install all dependencies
- Start the application

#### Option 2: Manual Setup
1. **Clone or navigate to this directory**:
   ```bash
   cd markdown-previewer
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser**:
   Navigate to `http://localhost:5000`

That's it! You should see the Markdown Live Previewer interface.

## 📖 Usage Guide

### Basic Usage
1. **Start typing** markdown in the left editor pane
2. **Watch the preview** update automatically on the right
3. **Use the toolbar** for file operations and theme switching

### Saving Files
1. Click the "💾 Save" button in the header
2. Enter a filename (or use the default)
3. Press "Save" - files are saved to your Downloads folder

### Loading Files
1. Click the "📂 Open" button
2. Select a `.md` or `.txt` file
3. The content will load into the editor

### Changing Themes
- Click the "🌓 Theme" button to toggle between dark and light modes
- The syntax highlighting theme automatically adjusts

## 🎨 Supported Markdown Features

### Text Formatting
```markdown
**Bold** *Italic* ~~Strikethrough~~
`Inline Code`
```

### Headers
```markdown
# H1
## H2
### H3
```

### Lists
```markdown
- Unordered list
- Another item

1. Ordered list
2. Another item

- [ ] Task list
- [x] Completed task
```

### Code Blocks
````markdown
```python
def hello_world():
    print("Hello!")
```
````

### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

### Links & Images
```markdown
[Link Text](https://example.com)
![Alt Text](image.jpg)
```

### Blockquotes
```markdown
> This is a blockquote
```

## 🏗️ Project Structure

```
markdown-previewer/
├── app.py              # Flask backend server
├── templates/
│   └── index.html      # Frontend HTML/CSS/JS
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask 3.0
- **Markdown Engine**: Python-Markdown with multiple extensions
- **API Endpoints**:
  - `GET /` - Main page
  - `POST /api/preview` - Convert markdown to HTML
  - `GET /api/load` - Load current content
  - `POST /api/save` - Save to file
  - `POST /api/upload` - Load from file

### Frontend
- **Vanilla JavaScript** (no frameworks!)
- **Highlight.js** for syntax highlighting
- **CSS Grid & Flexbox** for layout
- **CSS Custom Properties** for theming

### Markdown Extensions
- `fenced_code` - GitHub-style code blocks
- `tables` - Table support
- `codehilite` - Code syntax highlighting
- `toc` - Table of contents generation
- `nl2br` - Newline to `<br>` conversion
- `sane_lists` - Better list handling
- `extra` - Various useful extensions

## 🎯 Use Cases

Perfect for:
- **Technical Writing**: Documentation, tutorials, README files
- **Note Taking**: Quick markdown notes with instant preview
- **Blog Writing**: Draft blog posts in markdown
- **Learning Markdown**: See markdown syntax rendered in real-time
- **GitHub README Development**: Preview how your README will look

## 🐛 Troubleshooting

### Port 5000 Already in Use
If you see an error about port 5000 being in use:
```bash
# Change the port in app.py (last line):
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Dependencies Not Installing
Make sure you have Python 3.7+ and pip installed:
```bash
python --version
pip --version
```

### Preview Not Updating
- Check your browser console for errors
- Make sure JavaScript is enabled
- Try refreshing the page

## 🚀 Future Enhancements

Potential additions:
- [ ] Export to PDF
- [ ] Export to HTML
- [ ] Multiple file tabs
- [ ] Git integration
- [ ] Collaborative editing
- [ ] Custom themes
- [ ] Markdown templates
- [ ] Image upload support
- [ ] Auto-save functionality
- [ ] Vim/Emacs keybindings

## 📝 Development

Want to extend or modify the app? Here's how:

1. **Backend changes**: Edit `app.py`
2. **Frontend changes**: Edit `templates/index.html`
3. **Add extensions**: Modify the markdown extensions in `app.py`
4. **Styling**: Edit the `<style>` section in `index.html`

## 🤝 Contributing

Feel free to fork, modify, and improve! This is a learning project designed to be:
- Easy to understand
- Easy to extend
- Well-documented

## 📄 License

MIT License - Feel free to use this however you like!

## 🌟 Credits

Created as part of the mini-projects collection by Jarvis.

**Technologies Used**:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Python-Markdown](https://python-markdown.github.io/) - Markdown parser
- [Highlight.js](https://highlightjs.org/) - Syntax highlighting
- [Pygments](https://pygments.org/) - Python syntax highlighting

---

**Made with ❤️ and markdown**

Start writing beautiful documentation today! 📝✨
