---
sidebar_position: 2
sidebar_label: 'React UI basics'
---

# React UI basics

Spotify Plus renders React components as native Android views. You can build an extension-owned screen, or use the same components in a Spotify page replacement. This tutorial creates a small drawer-launched screen; follow [Creating a custom UI page](./custom-ui-page.md) for replacements and overlays, or [Writing native views in Java](./native-ui.md) for your own Android view types.

React state and effects work as usual. The UI primitives and style/event APIs come from `spotifyplus/react`, not browser HTML or `react-native`. Familiar React Native layout concepts are useful, but only Spotify Plus's exported components and props are supported.

## Build a screen

Use a `.tsx` file for JSX. This screen uses state, a scroll container with one wrapper view, and native-backed buttons.

```tsx title="src/app.tsx"
import React, { useState } from 'react';
import { View, Text, Button, ScrollView } from 'spotifyplus/react';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <View style={{ flex: 1, backgroundColor: '#121212' }}>
      <ScrollView style={{ flex: 1 }}>
        <View style={{ width: '100%', padding: 24, gap: 12 }}>
          <Text style={{ color: '#ffffff', fontSize: 24 }}>My extension</Text>
          <Text style={{ color: '#bbbbbb' }}>Pressed {count} times</Text>
          <Button text="Press me" onPress={() => setCount(value => value + 1)} />
          <Button text="Reset" onPress={() => setCount(0)} />
        </View>
      </ScrollView>
    </View>
  );
}
```

Use numeric layout values for the renderer's density-aware sizing, percentage widths when appropriate, and flex to occupy available space. Keep raw text inside `Text`. Native drawing inside a custom Java view uses Android pixel coordinates and must do its own conversion.

## Open it from a side drawer button

Return a React element from the drawer callback to open an extension-owned screen. This does not replace Spotify Home or the native drawer layout.

```tsx title="src/index.tsx"
import { SpotifyPlus } from 'spotifyplus';
import App from './app';

new SpotifyPlus.SideDrawer('My extension', () => <App />).register();
```

Register the entry once at extension load. An optional third constructor argument supplies an icon from `SpotifyPlus.Assets.image()`. See [SideDrawer](../spotifyplus-api/side-drawer.md) for the reference.

## Mount content on a Spotify screen

The `UI` methods accept a component type, rather than a rendered element. Check both target availability and its supported operation.

```tsx
import { SpotifyPlus } from 'spotifyplus';
import { View, Text } from 'spotifyplus/react';

function LyricsBadge() {
  return (
    <View pointerEvents="none" style={{
      position: 'absolute', top: 16, right: 16, padding: 8,
      backgroundColor: '#333333', borderRadius: 8,
    }}>
      <Text style={{ color: '#ffffff' }}>Lyrics badge</Text>
    </View>
  );
}

async function installBadge() {
  const info = await SpotifyPlus.UI.inspect('lyrics.page');
  if (!info.available || !info.operations.includes('overlay')) return;

  return SpotifyPlus.UI.overlay('lyrics.page', LyricsBadge);
}

void installBadge().catch(console.error);
```

This puts the badge on top of the lyrics page whenever the user opens it. Using `lyrics.page` is what tells Spotify Plus that is where you want to put it. You can keep a reference to that overlay in a variable if you want to get rid of it at some point.

If you want to completely change a page, or other parts of Spotify's UI, you can check out [how to create a custom page](./custom-ui-page.md).