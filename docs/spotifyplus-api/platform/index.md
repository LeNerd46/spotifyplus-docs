---
sidebar_label: 'Platform data'
---

# Platform data

`SpotifyPlus.Platform` exposes device information, the current Spotify session, the clipboard, and extension storage.

## PlatformData

```ts
const { clientVersion, osName, osVersion, sdkVersion } = SpotifyPlus.Platform.PlatformData;
console.log(clientVersion, osName, osVersion, sdkVersion);
```

`clientVersion` is the Spotify app version. `osName`, `osVersion`, and `sdkVersion` describe the Android device.

## Session

```ts
const accessToken = SpotifyPlus.Platform.Session.accessToken;
```

`accessToken` is the current user's Spotify access token. Keep it within the extension and use it only for requests the user expects.
