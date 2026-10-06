from pathlib import Path

path = Path(__file__).parent / 'rework_examples.py'
content = path.read_text(encoding='utf-8')
start = content.index('\nTYPE_LINKS = {')
marker = "print(f'Reworked {len(paths)} method pages')"
end = content.index(marker, start) + len(marker)
block = content[start:end]
path.write_text(content[:start] + content[end:] + block + '\n', encoding='utf-8')
