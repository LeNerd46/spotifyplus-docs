---
sidebar_label: 'Event payloads'
---

# Event payloads

`SpotifyPlus.Events` broadcasts Spotify state changes to extensions. Custom events emitted with `Events.emit()` stay inside the emitting extension.

| Event | Payload |
| --- | --- |
| `contextChanged` | `{ uri: string; previousUri: string }` |
| `songChanged` | `{ uri: string \| null; previousUri: string \| null }` |
| `playPause` | `{ isPlaying: boolean; isPaused: boolean }` |
| `trackSeeked` | `{ positionMs: number; previousPositionMs: number }` |
| `shuffleChanged` | `{ enabled: boolean }` |
| `repeatChanged` | `{ mode: RepeatMode }` |
| `deviceChanged` | `{ device: ConnectDevice \| null; previousDeviceId: string \| null }` |

`trackSeeked` fires for an acknowledged local seek or a remote position jump greater than 1.5 seconds. Use the same handler function when calling `Events.off()`.
