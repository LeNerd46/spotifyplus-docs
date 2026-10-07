---
sidebar_label: 'ContextMenu'
---

# ContextMenu

Register extension actions in Spotify's menus or open a native menu from custom UI. To replace a menu layout, use [UI targets](./ui/index.md).

## Register an action

```ts
new SpotifyPlus.ContextMenu(
  name: string,
  onClick: (uri: string) => void,
  shouldAdd?: (uri: string, contextUri: string) => boolean,
  disabled?: boolean,
  types?: 'track' | 'artist' | 'album' | 'playlist' |
    readonly ('track' | 'artist' | 'album' | 'playlist')[]
).register()
```

```ts
import { SpotifyPlus } from 'spotifyplus';

new SpotifyPlus.ContextMenu(
  'Copy item URI',
  uri => {
    try { SpotifyPlus.Platform.Clipboard.writeText(uri); }
    catch (error) { console.error(error); }
  },
  undefined,
  false,
  ['track', 'album'],
).register();
```

Arguments are positional. `register()` returns the item; creating an item alone does not register it. Omit `types` to allow every context, including unidentified kinds. An empty array allows none. Disabled items are hidden in the current modern hook.

`shouldAdd` is a quick, synchronous predicate: only boolean `true` shows the item. False, exceptions, and non-boolean results hide it. Promises/async predicates are unsupported. Use cached local state for metadata-dependent filtering rather than making a request during menu construction.

```ts
const allowedTrackUris = new Set<string>();
// Populate this set from your extension's state before a menu opens.
new SpotifyPlus.ContextMenu(
  'Saved action',
  uri => console.log('Selected', uri),
  uri => allowedTrackUris.has(uri),
  false,
  'track',
).register();
```

Visibility is reevaluated for each opening. The modern hook currently supplies the selected entity URI for both predicate arguments, or an empty string when unknown; the second argument is not a distinct parent URI. The entire visibility batch has a 150 ms timeout. On timeout, conditional items are hidden for that opening while unconditional enabled items remain.

## Open an item menu

```ts
SpotifyPlus.ContextMenu.open(
  item: SpotifyUriInput,
  options?: { contextUri?: SpotifyUriInput }
): Promise<void>
```

`item` accepts a track, album, artist, or playlist URI, Spotify URL, or object with `uri`. The optional `contextUri` accepts the same URI/URL/object shape and informs Spotify's context-dependent actions. See [SpotifyUriInput](../types/spotify-uri-input.md).

```tsx
import { Button } from 'spotifyplus/react';

function MoreOptions({ uri, parentUri }: { uri: string; parentUri?: string }) {
  return <Button text="More options" onPress={() => {
    void SpotifyPlus.ContextMenu.open({ uri }, { contextUri: parentUri })
      .catch(console.error);
  }} />;
}
```

The menu includes applicable extension entries and React menu contributions. Invalid arguments throw synchronously before dispatch. Launcher/readiness failures reject. Resolution acknowledges launching the menu, not completion of its asynchronous content loading.

## Open the Now Playing menu

```ts
SpotifyPlus.ContextMenu.openNowPlaying(): Promise<void>
```

```tsx
function NowPlayingOptions() {
  return <Button text="Now Playing options" onPress={() => {
    void SpotifyPlus.ContextMenu.openNowPlaying().catch(console.error);
  }} />;
}
```

This opens the context menu that you would get from the now playing screen. This has some additional options such as toggling the in line lyrics. And maybe other stuff, idk
