---
sidebar_label: 'seek()'
---

import Badge from '@site/src/components/Badge';

# Player.seek()

Moves playback to a specified position in the currently playing track

## Syntax

```ts
SpotifyPlus.Player.seek(position: number): void
```

## Examples

The following example will skip the song forward 10 seconds

```ts
const progress = SpotifyPlus.Player.getProgress();

SpotifyPlus.Player.seek(progress + 10_000);
```

The following example restarts the song from the beginning

```ts
SpotifyPlus.Player.seek(0);
```

The following example jumps to the halfway point of the current track

```ts
const track = SpotifyPlus.Player.getCurrentTrack();
SpotifyPlus.Player.seek(Math.floor(track.durationMs / 2));
```

## Parameters

`position`

<Badge>number</Badge> <Badge variant="danger">Required</Badge>

The desired playback position in milliseconds. It must be a non-negative safe integer.

## Returns

`void`

Returns after Spotify acknowledges the local command. Playback and state events may arrive later.

## Exceptions

| Exception   | Condition                                     |
| :--------   | :-------------------------------------------- |
| `TypeError` | The position is negative or an unsafe integer |


This is a synchronous local call. It throws if the player is not ready or Spotify rejects the command. Use `try/catch` for errors. Playback state and events can update after the call returns.
