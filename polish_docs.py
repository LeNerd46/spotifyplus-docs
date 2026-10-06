from pathlib import Path
import re

root = Path(__file__).parent / 'docs' / 'spotifyplus-api'
for path in root.rglob('*.mdx'):
    content = path.read_text(encoding='utf-8')
    old = 'The following example shows a typical use of this method in an extension.'
    if old in content:
        first_comment = re.search(r'## Examples\n\n' + re.escape(old) + r'\n\n```(?:ts|tsx)\n// (.+?)\n', content)
        if first_comment:
            action = first_comment.group(1).rstrip('.').strip()
            action = action[0].lower() + action[1:]
            content = content.replace(old, f'The following example shows how an extension can {action}.', 1)
    if '```tsx\n' in content and "import { Text } from 'spotifyplus/react';" not in content:
        imports = "import { Text } from 'spotifyplus/react';\n"
        if 'UIComponentProps' in content.split('## Examples', 1)[1].split('## Parameters', 1)[0]:
            imports = "import type { UIComponentProps } from 'spotifyplus';\n" + imports
        content = content.replace('```tsx\n', '```tsx\n' + imports + '\n', 1)
    if path.relative_to(root).as_posix() == 'assets/image.mdx':
        content = content.replace('() => <LikedSongsPanel />', "() => <Text>Liked Songs helper</Text>")
    path.write_text(content, encoding='utf-8')

intro = Path(__file__).parent / 'docs' / 'intro.mdx'
content = intro.read_text(encoding='utf-8')
content = content.replace('./spotifyplus-api/library/list.md)', './spotifyplus-api/library/list.mdx)')
intro.write_text(content, encoding='utf-8')
