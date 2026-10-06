---
sidebar_label: 'SideDrawer'
---

import Badge from '@site/src/components/badge';

# SideDrawer

Adds an item to Spotify's side drawer. Construct an item, then call `register()`.

## Syntax

```ts
new SpotifyPlus.SideDrawer(
  name: string,
  onClick: () => React.ReactElement | void,
  icon?: ExtensionAsset
).register(): SideDrawerItem
```

## Examples

```tsx
const icon = SpotifyPlus.Assets.image('images/panel.png');

new SpotifyPlus.SideDrawer( 'My panel', () => {
  return <MyPanel />
}, icon ).register();
```

## Parameters

`name`

<Badge>string</Badge> <Badge variant="danger">Required</Badge>

Visible drawer label.

`onClick`

<Badge>Function</Badge> <Badge variant="danger">Required</Badge>

Function to run when the user presses this side drawer item. If the function returns a React component, it will render that component.

`icon`

<Badge href='/docs/types/extension-assets'>ExtensionAsset</Badge> <Badge variant="neutral">Optional</Badge>

Icon to use for the button. If none is provided, defaults to a lightning icon.

## Returns

`register()` returns the registered drawer item.

## Remarks

You may want to show some sort of screen when the user presses a side drawer button. Returning a react component in your on click handler will render that react component. This is not required though, if you do not want to show a screen.

## Open the native drawer

```ts
SpotifyPlus.SideDrawer.open(): Promise<void>
```

```tsx
import { SpotifyPlus } from 'spotifyplus';
import { Button } from 'spotifyplus/react';

function OpenDrawer() {
  return <Button text="Open drawer" onPress={() => {
    SpotifyPlus.SideDrawer.open();
  }} />;
}
```

Opens the main activity's native drawer, including registered extension entries, even when Home is replaced. A `navigation.drawer` replacement still applies. Requires a foreground Spotify activity and ready native launcher; early startup, unsupported layouts, or unavailable activity state reject. Resolution acknowledges launch rather than completion of asynchronous native rendering. Current bindings target Spotify **9.1.82.2160**.

Returning a React element from a registered drawer entry opens an extension-owned screen; `SideDrawer.open()` opens Spotify's drawer itself. To customize that drawer, see [Creating a custom UI page](../guides/custom-ui-page.md#6-rebuild-a-drawer-or-menu-with-native-parts).
