---
sidebar_label: 'PlaybackState'
---

# PlaybackState

Defines the current playback state

## Syntax

```ts
interface PlaybackState {
    contextUri: string;
    trackUri: string | null;
    isPlaying: boolean;
    isPaused: boolean;
    isBuffering: boolean;
    positionMs: number;
    shuffle: boolean;
    repeat: RepeatMode;
}
```

## Remarks

This interface represents the current playback state of the Spotify player. It contains information such as the URI of the song playing, how far into the song the player is, and information such as play/pause, shuffle, and repeat state. 