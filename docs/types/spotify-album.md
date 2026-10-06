---
sidebar_label: 'SpotifyAlbumData'
---

# SpotifyAlbumData

Represents an album.

## Syntax

```ts
interface SpotifyAlbumData {
  title: string;
  artist: string;
  release?: Date;
  image: string;
}
```

## Example

```ts
const track = SpotifyPlus.Player.getCurrentTrack();
console.log(track.album.title, track.album.image);
```

## Remarks

For full album metadata, use `SpotifyPlus.Internal.getAlbum(albumUri)`.