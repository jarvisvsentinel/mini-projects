#!/usr/bin/env python3
"""
Markdown Live Previewer - A web-based markdown editor with live preview
Supports GitHub Flavored Markdown, syntax highlighting, and file operations
"""

from flask import Flask, render_template, request, jsonify
import markdown
from markdown.extensions import fenced_code, tables, codehilite, toc
import os
from pathlib import Path
import json

app = Flask(__name__)

# Configure markdown with GitHub Flavored Markdown extensions
md = markdown.Markdown(
    extensions=[
        'fenced_code',
        'tables',
        'codehilite',
        'toc',
        'nl2br',
        'sane_lists',
        'extra'
    ],
    extension_configs={
        'codehilite': {
            'css_class': 'highlight',
            'linenums': False,
            'guess_lang': True
        }
    }
)

# Store for temporary content (in production, use sessions or database)
content_store = {
    'markdown': '# Welcome to Markdown Previewer\n\nStart typing your markdown here...\n\n## Features\n\n- Live preview\n- GitHub Flavored Markdown\n- Syntax highlighting\n- Save/Load files\n- Dark/Light theme\n\n## Code Example\n\n```python\ndef hello_world():\n    print("Hello, Markdown!")\n```\n\n## Table Example\n\n| Feature | Status |\n|---------|--------|\n| Live Preview | ✓ |\n| GFM Support | ✓ |\n| Themes | ✓ |\n'
}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/preview', methods=['POST'])
def preview():
    """Convert markdown to HTML"""
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    
    # Reset markdown instance to clear any previous state
    md.reset()
    
    # Convert markdown to HTML
    html = md.convert(markdown_text)
    
    # Store the content
    content_store['markdown'] = markdown_text
    
    return jsonify({
        'html': html,
        'success': True
    })

@app.route('/api/load', methods=['GET'])
def load():
    """Load current markdown content"""
    return jsonify({
        'markdown': content_store.get('markdown', ''),
        'success': True
    })

@app.route('/api/save', methods=['POST'])
def save():
    """Save markdown to file"""
    data = request.get_json()
    markdown_text = data.get('markdown', '')
    filename = data.get('filename', 'document.md')
    
    # Ensure filename ends with .md
    if not filename.endswith('.md'):
        filename += '.md'
    
    # Save to user's home directory or specified path
    save_dir = Path.home() / 'Downloads'
    save_dir.mkdir(exist_ok=True)
    filepath = save_dir / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        return jsonify({
            'success': True,
            'message': f'Saved to {filepath}',
            'path': str(filepath)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving file: {str(e)}'
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload():
    """Load markdown from uploaded file"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        content_store['markdown'] = content
        
        # Reset markdown instance
        md.reset()
        html = md.convert(content)
        
        return jsonify({
            'success': True,
            'markdown': content,
            'html': html
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading file: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 Markdown Live Previewer")
    print("="*50)
    print("\n📝 Server starting at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
