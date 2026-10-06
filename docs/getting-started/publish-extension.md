---
sidebar_label: 'Publishing Your Extension'
sidebar_position: 2
---

Once you finish your extension, you probably want to publish it for others to use. This will go over how to publish it!

# Publishing Your Extension

To publish your extension to the marketplace, you need to have a GitHub repo for it. So you need to create a GitHub repo with your main extension file, and a `manifest.json`. Your manifest will tell the marketplace how/what to install, and extra information about it.

In order for your extension to show up in the maretkplace, you must give your repo the `spotifyplus-extensions` topic, and you must have a valid `manifest.json`.

# Example Manifest

Below is an example of a full `manifest.json`.

```json title="manifest.json"
{
  "id": "com.lenerd.bookmarks",
  "name": "Bookmarks",
  "description": "Allows you to save songs, albums, and artists for later!",
  "version": "1.0",
  "authors": [
    {
      "name": "LeNerd46",
      "url": "https://www.github.com/LeNerd46"
    }
  ],
  "tags": ["bookmarks", "library"],
  "preview": "screenshot.png",
  "changelog": "changelog.json",
  "banner": "banner.png",
  "api": 2,
  "assets": ["assets/**/*"],
  "main": "dist/index.js",
  "native": {
    "apk": "native.apk",
    "pluginClass": "com.lenerd.bookmarks.NativePlugin"
  }
}
```

# Manifest Properties

This is a list of all properties available in `manifest.json`

| Property      | Type             | Description                                               | Required |
| :------------ | :--------------- | :-------------------------------------------------------- | :------- |
| `id`          | `string`         | A unique identifier for your extension                    | ✓        |
| `name`        | `string`         | The name of your extension                                | ✓        |
| `description` | `string`         | A description of your extension                           | ✓        |
| `version`     | `string`         | What version your extension is on                         | ✓        |
| `authors`     | `Author[]`       | A list of authors who worked on this extension            | ✓        |
| `tags`        | `string[]`       | Tags used to categorize your extension                    | ✓        |
| `api`         | `number`         | What version of the Spotify Plus API this extension uses  | ✓        |
| `main`        | `string`         | Path to the main JavaScript file                          | ✓        |
| `preview`     | `string`         | Path to image used for a preview image in the marketplace |          |
| `banner`      | `string`         | Path to image used for a banner image in the marketplace  |          |
| `assets`      | `string[]`       | An array of assets used by your extension                 |          |
| `native`      | `NativeMetadata` | Information about the native code your extension uses     |          |
| `changelog`   | `Changelog`      | Your extension's changelog                                |          |

### Author

| Property | Type     | Description                                   | Required |
| :------- | :------- | :-------------------------------------------- | :------- |
| `name`   | `string` | The name of the author                        | ✓        |
| `url`    | `string` | A URL to the user's GitHub (or other) profile | ✓        |

### Native Metadata

| Property      | Type     | Description                        | Required |
| :------------ | :------- | :--------------------------------- | :------- |
| `apk`         | `string` | Path to the APK file               | ✓        |
| `pluginClass` | `string` | Full name of the entry point class | ✓        |

## Changelog

This is where you can define a changelog for your extension. This will appear in the marketplace. It is an array of changelog entries. Below is an example of a changelog

```json
[
  {
    "version": "1.1",
    "release": "2026-21-09",
    "sections": [
      {
        "heading": "Changes",
        "changes": [
          "Changed something",
          {
            "text": "There are also some related things that changed",
            "subLines": ["Here is one", "This is another!", "Oh boy, one more"]
          }
        ]
      },
      {
        "heading": "Fixed",
        "changes": [
          "Something was fixed",
          "Wait, there was another thing that got fixed"
        ]
      }
    ]
  },
  {
    "version": "1.0",
    "release": "2026-8-26",
    "sections": [
      {
        "heading": "New",
        "changes": ["Initial release"]
      }
    ]
  }
]
```

| Property   | Type                 | Description                                    | Required |
| :--------- | :------------------- | :--------------------------------------------- | :------- |
| `version`  | `string`             | What version this entry is                     | ✓        |
| `release`  | `string`             | The day this version was released (YYYY-MM-DD) | ✓        |
| `sections` | `ChangelogSection[]` | A list of sections                             | ✓        |

<br/>
| Property  | Type                                    | Description                  | Required |
| :-------- | :-------------------------------------- | :--------------------------- | :------- |
| `heading` | `string`                                | The heading for this section | ✓        |
| `changes` | `string[] \| ChangelogSectionChanges[]` | A list of changes            | ✓        |

<br/>
| Property   | Type       | Description        | Required |
| :--------- | :--------- | :----------------- | :------- |
| `text`     | `string`   | The top line       | ✓        |
| `subLines` | `string[]` | A list of sublines | ✓        |
