---
sidebar_label: 'SpotifyUriInput'
---

# SpotifyUriInput

Defines a Spotify URI parameter

## Syntax

```ts
type SpotifyUriInput = string | { uri: string };
```

## Remarks

If you see this, you can either pass in a direct uri (such as `spotify:track:4ABYxlb92WBIjHu7TIKmml`), or you can pass in the object directly, such as in the following example.

```ts
// Get a SpotifyTrack object
const track = SpotifyPlus.Player.getCurrentTrack();

// Pass the track object directly instead of using `track.uri`
SpotifyPlus.Queue.add(track);
```