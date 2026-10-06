---
sidebar_position: 3
sidebar_label: 'Writing native views'
---

# Writing native views in Java

Sometimes, you want to build something that you cannot do with regular React components. You need a deep level of customization, performance is essential, you need a complex view. Whatever the case is, sometimes you need to write these things in native code instead of JavaScript. This guide will go over how to setup your project for this, and how to create the views.

## 1. Set up the native project

When you created your extension, you had the option to have it set up the native project already. If you did that, great! You can skip this step. If not, don't worry. Setting it up is very simple. Simply run `npx spotifyplus create-native` and choose whatever language you want! For this guide, we will be using Java, because I like Java better and I am more familiar with it. Kotlin should work just as well though.

This tutorial uses the following layout; adapt paths to your generated project:

```text
my-extension/
  manifest.json
  src/index.tsx
  native/
    gradlew
    gradlew.bat
    lib/spotifyplus-sdk.aar
    app/build.gradle.kts
    app/src/main/java/com/example/meter/
      MeterView.java
      MeterComponent.java
      NativePlugin.java
  meter.apk
```

If you are creating the project manually, you need to add the Spotify Plus SDK to your project. Using the `npx` command will do this automatically. You can find the `.aar` file in the GitHub releases. Add it as **compileOnly**, as the SDK lives inside of Spotify Plus. Your extension does not need to add the SDK itself.

```kotlin title="native/app/build.gradle.kts"
dependencies {
    compileOnly(files("${rootDir}/lib/spotifyplus-sdk.aar"))
}
```

Your compiled APK should be shipped with your JavaScript, and that is what will be loaded in order for your views to exist inside of Spotify.

## 2. Write the Android view

Now you can create your view! This can just be any view. Whatever view you wanted to make, you can do it here. Here, I am creating a meter view.

```java title="MeterView.java"
package com.example.meter;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

public final class MeterView extends View {
    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private float progress = 0f;
    private int accent = Color.rgb(30, 215, 96);
    private String label = "Progress";

    public MeterView(Context context) {
        super(context);

        setWillNotDraw(false);
        updateAccessibility();
    }

    public void setMeter(float progress, int accent, String label) {
        this.progress = Math.max(0f, Math.min(1f, progress));
        this.accent = accent;
        this.label = label;

        updateAccessibility();
        invalidate();
    }

    private void updateAccessibility() {
        setContentDescription(label + ": " + Math.round(progress * 100) + "%");
    }

    private float dp(float value) {
        return value * getResources().getDisplayMetrics().density;
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float inset = dp(8);
        float left = inset;
        float right = Math.max(left, getWidth() - inset);
        float top = Math.min(inset, getHeight() / 2f);
        float bottom = Math.max(top, getHeight() - inset);
        float radius = dp(6);

        paint.setColor(Color.rgb(50, 50, 50));
        canvas.drawRoundRect(left, top, right, bottom, radius, radius, paint);
        paint.setColor(accent);
        canvas.drawRoundRect(left, top, left + (right - left) * progress, bottom, radius, radius, paint);
    }

    public void release() {
        // Stop native animators, remove callbacks/listeners, and cancel any
        // view-owned work here if those are added later. This view owns none.
    }
}
```

Try to avoid network requests, disk reads, or expensive work in constructors, `onDraw`, or prop updates. Your view runs on the main UI. You don't want to stall the app or lag the UI. 

## 3. Tell Spotify Plus it exists

In order to use your component, you have to tell Spotify Plus how to handle it. This class is where you will create the view, and handle prop updates. There are a few functions available. You are required to have `getName()`, `createView()`, and `updateProps()`. In `getName()`, you can just return a string with whatever name you want your component to have. This is what you will use in your JavaScript code. `createView()` is where you create your view that you wrote. `updateProps()` is where the props you pass in inside of your React component will show up. They are passed as a JSON object. 

Create `MeterComponent.java`. The SDK requires `getName()` and `createView()`. `updateProps()` translates JSON props into Java state; `onDropView()` handles disposal.

```java title="MeterComponent.java"
package com.example.meter;

import android.content.Context;
import android.graphics.Color;
import android.view.View;
import com.lenerd.spotifyplus.sdk.SpotifyPlusComponent;
import com.lenerd.spotifyplus.sdk.spotify.SpotifyPlusContext;
import org.json.JSONObject;

public final class MeterComponent extends SpotifyPlusComponent<MeterView> {
    @Override
    public String getName() {
        return "ExampleMeter";
    }

    @Override
    public MeterView createView(Context context, SpotifyPlusContext spotify) {
        return new MeterView(context);
    }

    @Override
    public void updateProps(MeterView view, JSONObject oldProps, JSONObject newProps) {
        // Check what props are in the JSON object, and adjust your view accordingly
        double raw = newProps.optDouble("progress", 0.0);
        float progress = Double.isFinite(raw) ? (float) raw : 0f;
        String label = newProps.optString("label", "Progress");
        int accent = Color.rgb(30, 215, 96);

        try {
            accent = Color.parseColor(newProps.optString("accent", "#1ed760"));
        } catch (IllegalArgumentException ignored) {
            // Invalid color strings use the default.
        }

        view.setMeter(progress, accent, label);
    }

    @Override
    public void onDropView(View view) {
        // This gets called whenever your view disappears. This is not required
        ((MeterView) view).release();
    }
}
```

## 4. Register it in the plugin

Now that Spotify Plus knows how to handle it, there is one last step. You have to register it! This allows Spotify Plus to know your component actually exists. Registering is a pretty simple process.

Go to the entry point of your project, and register it in the `register()` function. Keep note of the name of this class. You will need it in your `manifest.json`

```java title="NativePlugin.java"
package com.example.meter;

import com.lenerd.spotifyplus.sdk.SpotifyPlusPlugin;
import com.lenerd.spotifyplus.sdk.SpotifyPlusRegistry;
import com.lenerd.spotifyplus.sdk.spotify.SpotifyPlusContext;

public final class NativePlugin implements SpotifyPlusPlugin {
    public NativePlugin() { }

    @Override
    public void register(SpotifyPlusRegistry registry, SpotifyPlusContext context) {
        // We are registering the component here. This is `SpotifyPlusComponent` NOT the Android view itself
        registry.registerComponent(new MeterComponent());
    }
}
```

## 5. Add the native APK to the extension manifest

For Spotify Plus to find your native code, you have to tell it that you have native code. In your `manifest.json`, add a new `native` section. In here, you will tell it the path to your compiled APK and the main entry class to your plugin. The APK path is relative to your main JavaScript path. The `pluginClass` is the ful. name of the entry class, the class that implements `SpotifyPlusPlugin`.

```json title="manifest.json"
{
  "id": "com.example.meter",
  "name": "Native Meter",
  "description": "A native meter used from React",
  "version": "1.0.0",
  "api": 2,
  "main": "dist/index.js",
  "native": {
    "apk": "meter.apk",
    "pluginClass": "com.example.meter.NativePlugin"
  }
}
```

## 6. Create the typed React wrapper

Now that you have the native code all set up, you can use it inside of your React code! First, if you have any props, you can make an interface so that you have types. Then simply call `createNativeComponent()`. Include the same name that you returned in `getName()` in your native code. In this case, mine was `ExampleMeter`.

```tsx title="src/index.tsx"
import React, { useState } from 'react';
import { SpotifyPlus } from 'spotifyplus';
import { createNativeComponent, View, Text, Button } from 'spotifyplus/react';

interface MeterProps {
  progress?: number;
  accent?: string;
  label?: string;
}

const Meter = createNativeComponent<MeterProps>('ExampleMeter');

function MeterDemo() {
  const [progress, setProgress] = useState(0.25);

  return (
    <View style={{ flex: 1, padding: 24, backgroundColor: '#121212' }}>
      <Text style={{ color: '#ffffff', fontSize: 24 }}>Native meter</Text>
      <Meter progress={progress} accent="#1ed760" label="Demo progress" style={{ width: '100%', height: 48, marginVertical: 16 }} />
      <Button text="Advance" onPress={() => {
        setProgress(value => value >= 1 ? 0 : Math.min(1, value + 0.25));
      }} />
    </View>
  );
}

new SpotifyPlus.SideDrawer('Native meter demo', () => <MeterDemo />).register();
```

Now when you press the `Native meter demo` button in teh side drawer and press `Advance`, it will change the React state. It will then send new JSON props, and redraws the same native view.

And that's it! Now you have a custom native React component. You can use this anywhere you want, as it is just a normal React component at this point.

To build your native code, you can run `npm run build:native`.

## Synchronous local APIs

Player controls (`seek`, `play`, `pause`, skips, shuffle, repeat), `Player.getState()`, Queue methods, Library membership and edits, playlist creation and edits, Connect device snapshots, clipboard methods, and Storage reads return directly. Commands return `void`; getters return their value. Native service errors throw synchronously:

```ts
try {
  const track = SpotifyPlus.Player.getCurrentTrack();
  const liked: boolean = SpotifyPlus.Library.isLiked(track);
  SpotifyPlus.Player.seek(30_000);
  SpotifyPlus.toast(liked ? 'Already liked' : 'Not liked');
} catch (error) {
  SpotifyPlus.toast(String(error));
}
```

Remove `.then()`/`.catch()` chains from local API calls and use `try/catch`. `await` still accepts direct values, but is unnecessary. Calls wait for the local service acknowledgement (local RPCs have a 15-second timeout), while playback, emitted state events, and account synchronization can happen later. Avoid repeated native queries in render functions; read state in effects or event handlers.

Search, Internal metadata, User profile, Library listing, playlist loading with `Playlists.get()`, context playback, and Connect transfer keep their Promises because they may load data or coordinate network work. Native UI launch, inspection, and action calls keep Promises because they run on Android's main thread and may need callbacks from the extension. `Events.emit()` also keeps its Promise so callers can wait for async listeners.
