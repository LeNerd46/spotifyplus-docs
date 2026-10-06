---
sidebar_label: 'API result types'
---

# API result types

These types describe the results of search, library, playlist, queue, Connect, and user methods.

## SearchOptions

```ts
interface SearchOptions { 
  limit?: number; 
  locale?: string;
}
```

## SearchResponse

```ts
interface SearchResponse { 
  query: string; 
  items: SearchResult[];
}

interface SearchResult { 
  uri: string; 
  text: string;
}
```

## PageOptions

```ts
interface PageOptions { 
  offset?: number; 
  limit?: number;
}
```

## Page

```ts
interface Page<T> { 
  items: T[]; 
  offset: number; 
  limit: number; 
  total: number;
}
```

## LibraryItem

```ts
interface LibraryItem { 
  uri: string; 
  name: string; 
  imageUri: string; 
  pinned: boolean; 
}
```

## PlaylistPage

```ts
interface PlaylistItem { 
  uri: string; 
  rowId: string; 
  name: string; 
  addedAt: number; 
}

interface PlaylistPage extends Page<PlaylistItem> {
  uri: string; 
  name: string; 
  description: string; 
  ownedBySelf: boolean;
}
```

`rowId` identifies one occurrence of a track in a playlist. Use it for `removeTracks()` and `moveTracks()`.

## QueueSnapshot

```ts
interface QueueSnapshot {
  revision: string; 
  current: QueueEntry | null;
  next: QueueEntry[]; 
  previous: QueueEntry[];
}

interface QueueEntry { 
  uri: string; 
  uid: string; 
  metadata: Record<string, string>; 
}
```

Queue edits use `revision` to detect a change since the snapshot was fetched. Read a fresh snapshot before retrying an edit that was rejected.

## ConnectDevice

```ts
interface ConnectDevice {
  id: string; 
  name: string; 
  type: string; 
  isActive: boolean;
  isLocal: boolean; 
  isDisabled: boolean; 
  supportsVolume: boolean;
  volume: number; // Can be a value between 0 and 65535
}
```

## SpotifyUser

```ts
interface SpotifyUser {
  username: string; 
  displayName: string; 
  uri: string;
  images: Array<{ url: string; width: number; height: number }>;
}
```
