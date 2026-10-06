---
sidebar_label: 'NavigationOptions'
---

# NavigationOptions

Options for `SpotifyPlus.Navigation.open()`.

```ts
type NavigationTarget = 'auto' | 'spotify' | 'external';
interface NavigationOptions { target?: NavigationTarget }
```

`auto` chooses the best available app and is the default. `spotify` opens the link in Spotify, and `external` hands it to another app.

```ts
SpotifyPlus.Navigation.open('spotify:album:4aawyAB9vmqN3uQ7FjRGTy', {
  target: 'spotify'
});
```
