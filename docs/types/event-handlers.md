---
sidebar_label: 'Event handlers'
---

# Event handlers

Event callbacks may run synchronously or return a promise.

```ts
type EventHandler = (payload: unknown) => void | Promise<void>;
type ExtensionEventHandler<TPayload = unknown> = (payload: TPayload) => void | Promise<void>;
```

Spotify state events have typed payloads when you use `SpotifyPlus.Events.on()` with a known event name. Pass the same callback to `off()` when you want to unsubscribe.

```ts
const onShuffle = ({ enabled }: { enabled: boolean }) => SpotifyPlus.log(enabled);

SpotifyPlus.Events.on('shuffleChanged', onShuffle);
SpotifyPlus.Events.off('shuffleChanged', onShuffle);
```
