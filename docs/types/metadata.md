---
sidebar_label: 'Metadata results'
---

# Metadata results

`SpotifyPlus.Internal` returns normalized metadata. Each result also has a `raw` field containing Spotify's original response.

## Shared metadata fields

```ts
interface MetadataImage { 
  fileId: string; 
  size: string; 
  width: number; 
  height: number; 
  url: string;
}

interface MetadataArtistRef { 
  uri: string; 
  name: string;
}

interface MetadataDisc { 
  number: number; 
  tracks: string[];
}

interface MetadataDate { 
  year: number; 
  month: number; 
  day: number
}
```

## MetadataAlbum

```ts
interface MetadataAlbum {
  uri: string; 
  name: string; 
  image: string; 
  images: MetadataImage[];
  artists: MetadataArtistRef[]; 
  label: string; 
  type: string;
  popularity: number; 
  date: MetadataDate; 
  discs: MetadataDisc[];
  raw: Record<string, any>;
}
```

## MetadataArtist

```ts
interface MetadataArtist {
  uri: string; 
  name: string; 
  image: string; 
  images: MetadataImage[];
  popularity: number; 
  topTracks: Array<{ country: string; tracks: string[] }>;
  albums: string[]; 
  singles: string[]; 
  compilations: string[];
  appearsOn: string[]; 
  raw: Record<string, any>;
}
```

## MetadataPlaylist

```ts
interface MetadataPlaylist {
  uri: string; 
  revision: string; 
  name: string; 
  picture: string;
  description: string; 
  ownerUsername: string; 
  length: number;
  position: number; 
  truncated: boolean; 
  timestamp: string;
  createdAt: string; 
  isUserCreated: boolean; 
  canEditItems: boolean;
  canEditMetadata: boolean; 
  items: MetadataPlaylistItem[];
  raw: Record<string, any>;
}

interface MetadataPlaylistItem {
    uri: string; 
    addedBy: string; 
    timestamp: string; 
    itemId: string;
  }
```