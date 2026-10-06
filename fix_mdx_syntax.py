from pathlib import Path
import re

root = Path(__file__).parent / 'docs' / 'spotifyplus-api'
for path in root.rglob('*.mdx'):
    content = path.read_text(encoding='utf-8')
    def escape_braces(match):
        return match.group(0).replace('{', '&#123;').replace('}', '&#125;')
    content = re.sub(r'<span style=\{\{ display: \'inline\' \}\}>.*?</span>', escape_braces, content, flags=re.S)
    # The style expression itself must remain JSX.
    content = content.replace('<span style=&#123;&#123; display: \'inline\' &#125;&#125;>', "<span style={{ display: 'inline' }}>")
    content = re.sub(r'<Badge(?: [^>]*)?>.*?</Badge>', escape_braces, content, flags=re.S)
    path.write_text(content, encoding='utf-8')
