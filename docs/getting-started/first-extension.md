---
sidebar_label: 'First Extension'
sidebar_position: 0
---

Extensions are how you can modify or extend Spotify's features. They are JavaScript files that run along side Spotify's native code, and they let you modify Spotify however you'd like.

# Creating Your First Extension

Creating extensions are a pretty straight forward process. To create your extension, run `npx create-spotifyplus-app [extension-name]`. This will set up your extesnion for you. You will need to create a unique ID for your extesnion. This follows traditional package naming (com.company.name).

It will ask if you need native code. If you need more complex views or you need access to native Android functions, you will need native code. It can set this up for you. You can always add native code later. 

Once your extension is created, you can go check out `manifest.json`. This is where you can configure details about your extension. 

```json title="manifest.json"
{
    "id": "com.example.myextension", // Your extension's ID
    "name": "Example Extension", // The name of your extension
    "description": "Creating extensions is fun!", // A description of what your extension does
    "version": "1.0.0", // What version your extension is
    "authors": [ // An array of authors. Their name and a link to their GitHub (or other) profile
        {
            "name": "Author",
            "url": "https://www.github.com/Author"
        }
    ],
    "tags": [ // Tags to help find your extension
        "example"
    ],
    "api": 2, // What version of the Spotify Plus API your extension uses
    "main": "dist/index.js", // The main entry point of your extension
    "native": { // If your extension uses native code, you will need to include this
        "apk": "lyrics.apk", // Path to your APK file
        "pluginClass": "com.lenerd.lyricsnative.NativePlugin" // The main entry point to your native code
    }
}
```

Now your extension is all set up! Have fun building!