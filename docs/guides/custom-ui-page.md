---
sidebar_position: 4
sidebar_label: "Changing Spotify's UI"
---

# Changing Spotify's UI

This guide will go over how to change Spotify's UI. We will be changing the home page specifically in this guide, but there are many other pages you can change as well!

When you change any of Spotify's UI, your React code will live inside of the original UI's layout. Opening the page will create your UI, leaving the page will destroy your UI. 

## 1. Choose what page you want to change

Spotify changes its code a lot with every update, so it is not always guaranteed that the UI you want to change will actually be available. You can see information about each page by inspecting it. This will tell you if it's available, what you can do to it, and more.

```ts
import { SpotifyPlus } from 'spotifyplus';

async function inspectHome() {
  const info = await SpotifyPlus.UI.inspect('home.page');
  console.log(info.available, info.operations, info.instances, info.reason);
}

void inspectHome().catch(console.error);
```

In this case, the home page supports replacing it and overlaying UI on top of it. In order to see what UI targets are availalbe, see [the support table](../spotifyplus-api/ui/index.md#supported-boundaries).

This is a table explaining what each operation means. 

| Operation | Use it when |
| --- | --- |
| `replace` | You want to own the target layout or wrap its live native content |
| `overlay` | You want content above the target while its base content remains |
| `insertBefore` / `insertAfter` | The boundary explicitly supports ordered content around its native/replaced region |

Page targets do not support before/after insertions. Always check the operation you intend to use, not just `available`.

## 2. Build a replacement component

Now you can actually write your UI. In this case, we are going to replace the home page with our own home page. We will build our own home page, but also have an option to restore the original Spotify home page. The user will be able to toggle between the two here.

```tsx title="src/home-page.tsx"
import React, { useState } from 'react';
import { SpotifyPlus, type UIComponentProps } from 'spotifyplus';
import { View, Text, Button, ScrollView } from 'spotifyplus/react';

const report = (error: unknown) => console.error('Custom Home:', error);

export function HomePage({ context, Original }: UIComponentProps) {
  const [showNative, setShowNative] = useState(false);

  return (
    <View style={{ flex: 1, backgroundColor: '#121212' }}>
      <View style={{ padding: 16, gap: 8 }}>
        <Text style={{ color: '#ffffff', fontSize: 24 }}>My Home</Text>

        <Button text={showNative ? 'Show custom Home' : 'Show Spotify Home'} onPress={() => setShowNative(value => !value)} />

        <Button text="Open drawer" onPress={() => {
          SpotifyPlus.SideDrawer.open().catch(report);
        }} />
      </View>
      
      <View style={{ flex: 1 }}>
        {showNative ? <Original /> : (
          <ScrollView style={{ flex: 1 }}>
            <View style={{ width: '100%', padding: 16, gap: 12 }}>
              <Text style={{ color: '#ffffff' }}>
                {context.title ?? 'Your custom starting point'}
              </Text>

              <Text style={{ color: '#bbbbbb' }}>
                Page: {context.pageUri ?? context.uri ?? 'URI unavailable'}
              </Text>
              
              <Button text="Open Now Playing" onPress={() => {
                if (!SpotifyPlus.Navigation.openSpotify('spotify:now-playing')) {
                  console.warn('Now Playing navigation was not accepted');
                }
              }} />
              
              <Button text="Previous track" onPress={() => {
                try { SpotifyPlus.Player.skipPrevious(); } catch (error) { report(error); }
              }} />
              
              <Button text="Play / pause" onPress={() => {
                try { SpotifyPlus.Player.togglePlay(); } catch (error) { report(error); }
              }} />

              <Button text="Next track" onPress={() => {
                try { SpotifyPlus.Player.skipNext(); } catch (error) { report(error); }
              }} />
            </View>
          </ScrollView>
        )}
      </View>
    </View>
  );
}
```

A `ScrollView` has one wrapper `View`, and the outer page fills its available space. To have our button open the full now playing screen, we use `Navigation.openSpotify('spotify:now-playing')`. We can then write our own custom page for this by replacing `nowPlaying.page` if we wanted to.

`Original` is Spotify's original UI. This is a React component, so you can place it wherever you'd like. In the following example, we are placing a banner above the original Spotify home page. 

```tsx
import { type UIComponentProps } from 'spotifyplus';
import { View, Text } from 'spotifyplus/react';

function WrappedHome({ Original }: UIComponentProps) {
  return (
    <View style={{ flex: 1 }}>
      <Text style={{ padding: 12 }}>A banner above Spotify Home</Text>
      <View style={{ flex: 1 }}><Original /></View>
    </View>
  );
}
```

## 3. Install, toggle, and restore the replacement

You can then register your replacement, as in the following example. It checks support, avoids duplicate/pending registrations, and allows the user to bring the original Spotify home page back. You only want to register this once, do not register on every react rerender.

```tsx title="src/index.tsx"
import { SpotifyPlus, type UIRegistration } from 'spotifyplus';
import { HomePage } from './home-page';

let home: UIRegistration | undefined;
let installing = false;
let generation = 0;

async function enableHome() {
  if (home || installing) return;

  installing = true;
  const requestGeneration = generation;
  
  try {
    const info = await SpotifyPlus.UI.inspect('home.page');
    if (requestGeneration !== generation) return;
    
    if (!info.available || !info.operations.includes('replace')) {
      SpotifyPlus.warn(info.reason ?? 'Home replacement is unavailable');
      return;
    }
    
    home = SpotifyPlus.UI.replace('home.page', HomePage);
  } finally {
    installing = false;
  }
}

function restoreHome() {
  generation++; // Cancels an enable request still waiting for inspect().
  home?.dispose();
  home = undefined;
}

new SpotifyPlus.SideDrawer('Enable custom Home', () => {
  void enableHome().catch(console.error);
}).register();
new SpotifyPlus.SideDrawer('Restore Spotify Home', restoreHome).register();

// Uncomment to enable automatically on extension load:
// void enableHome().catch(console.error);
```

Now you can go to the side drawer, press `Enable custom home`, and go back home. You should see that your home page has changed now!

## 4. Add an overlay

An overlay is UI that you are putting on top of existing Spotify UI. This UI will be laid out independently of whatever Spotify has. There is no `Original` component because the original UI is already there, you are simply adding UI on top of it.

The following example will place a small badge on top of the lyrics page.

```tsx
import { SpotifyPlus, type UIRegistration } from 'spotifyplus';
import { View, Text } from 'spotifyplus/react';

function HomeBadge() {
  return (
    <View pointerEvents="none" style={{
      position: 'absolute', right: 16, bottom: 16,
      padding: 8, borderRadius: 8, backgroundColor: '#333333',
    }}>
      <Text style={{ color: '#ffffff' }}>Custom Home enabled</Text>
    </View>
  );
}

let badge: UIRegistration | undefined;
async function enableBadge() {
  if (badge) return;
  const info = await SpotifyPlus.UI.inspect('home.page');
  if (badge || !info.available || !info.operations.includes('overlay')) return;

  badge = SpotifyPlus.UI.overlay('home.page', HomeBadge);
}

new SpotifyPlus.SideDrawer('Show Home badge', () => {
  void enableBadge().catch(console.error);
}).register();
new SpotifyPlus.SideDrawer('Hide Home badge', () => {
  badge?.dispose();
  badge = undefined;
}).register();
```

You can add `pointerEvents="none"` if you do not want a component of your overlay to block touches. If your overlay does block touches, make sure it does not take up the whole screen unless if it needs to, otherwise you will not be able to interact with the Spotify UI underneath.

## 5. Open native menus from custom content

If you replace the home page with your own home page, you probably want to have some sort of way to open the side drawer, otherwise the user would not be able to access the marketplace, settings, or any other content that is there. Extensions are able to open the side drawer on their own for this.

You can simply just call `SpotifyPlus.SideDrawer.open()`. The same idea applies with context menus, however for the context menu, you have to provide some sort of URI so it knows what the context menu is for.

```tsx
import { SpotifyPlus } from 'spotifyplus';
import { View, Text, Button } from 'spotifyplus/react';

function ItemRow({ uri, title, contextUri }: {
  uri: string; title: string; contextUri?: string;
}) {
  const openMenu = () => {
    void SpotifyPlus.ContextMenu.open({ uri }, { contextUri })
      .catch(console.error);
  };

  return (
    <View onLongPress={openMenu} style={{ padding: 12 }}>
      <Text>{title}</Text>
      <Button text="Open" onPress={() => {
        SpotifyPlus.Navigation.openSpotify(uri);
      }} />
      <Button text="More options" onPress={openMenu} />
    </View>
  );
}
```

When using `ContextMenu.open()`, it has two options: a normal URI and a context URI. The normal URI is required. It opens the context menu for that item, whether it's a song, album, playlist, whatever. The context URI is for giving extra buttons depending on the context of where you're opening this context menu. For example, you will see different buttons when opening the context menu in the now playing view and in a playlist. You're giving it the same song, but if the context URI is a playlist URI, it will give you options related to that playlist that the now playing view would not give you.

Speaking of the now playing view, you can open that specific context menu by calling `ContextMenu.openNowPlaying()`. This has special options such as toggling the in line lyrics on. Otherwise, when you're opening a normal context menu, just pass in whatever the URI of the current page you're in for the context. If it's a playlist, pass in the playlist URI. If it's an album, pass in the album URI. That's what the context URI is for. I believe you can only open the now playing context menu inside of the now playing screen.

## 6. Create a custom side drawer or context menu

If you're replacing the context menu or the side drawer, you are pretty much starting from scratch. You probably still want the buttons that Spotify originally had there. Spotify Plus will give you those buttons through the context. Each button is a "part", and the context gives you a list of parts. If you want to keep the default Spotify context menu buttons, you can do so by creating a `<NativePart>` and passing through the IDs. This will have the original Spotify buttons.

```tsx
import { SpotifyPlus, type UIComponentProps } from 'spotifyplus';
import { ScrollView, View, Text } from 'spotifyplus/react';

function CustomDrawer({ context, NativePart }: UIComponentProps) {
  return (
    <ScrollView style={{ flex: 1 }}>
      <View style={{ width: '100%', padding: 16 }}>
        <Text style={{ fontSize: 24 }}>My navigation</Text>
        {(context.parts ?? []).map(part => (
          <NativePart key={part.id} id={part.id} />
        ))}
      </View>
    </ScrollView>
  );
}

async function installDrawer() {
  const info = await SpotifyPlus.UI.inspect('navigation.drawer');
  if (!info.available || !info.operations.includes('replace')) return;

  return SpotifyPlus.UI.replace('navigation.drawer', CustomDrawer);
}

void installDrawer().catch(console.error);
```

If you instead would like to create your own styled buttons, you can make your own Button, and have each button invoke an action with the ID of whatever button it is

```tsx
import { SpotifyPlus, type UIComponentProps } from 'spotifyplus';
import { ScrollView, View, Button } from 'spotifyplus/react';

function CustomMenu({ context, NativePart }: UIComponentProps) {
  return (
    <ScrollView style={{ flex: 1 }}>
      <View style={{ width: '100%', padding: 12 }}>
        {(context.parts ?? []).map(part => part.kind === 'content' ? (
          <NativePart key={part.id} id={part.id} />
        ) : (
          <Button key={part.id} text={part.title ?? part.semanticId} disabled={!part.enabled} onPress={() => {
              SpotifyPlus.UI.invokeAction(context.instanceId, part.id).catch(console.error);
          }} />
        ))}
      </View>
    </ScrollView>
  );
}

async function installMenu() {
  const info = await SpotifyPlus.UI.inspect('contextMenu.root');
  if (!info.available || !info.operations.includes('replace')) return;

  return SpotifyPlus.UI.replace('contextMenu.root', CustomMenu);
}

void installMenu().catch(console.error);
```