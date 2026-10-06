---
sidebar_label: 'Extension settings'
---

# Extension settings

ExtensionSettings defines an extension's settings page. Extension settings pages are split into different sectinos. You can either register settings one section at a time with `Settings.registerSetting()` or you can do it all at once with `Settings.registerSettings()`.

## ExtensionSettingSection

```ts
interface ExtensionSettingSection {
  title?: string;
  description?: string;
  items: ExtensionSettingItem[];
}
```

Most setting items have an `id`, `label`, optional `description` and `disabled`, plus a `type` and type-specific fields. Supported types are:

| Type | Main fields |
| --- | --- |
| `toggle` | `value: boolean` |
| `slider`, `number` | `value: number`, optional or required `min`, `max`, `step` |
| `text` | `value: string`, optional `placeholder`, `maxLength` |
| `select`, `radio` | `value: string`, `options: { label; value; description? }[]` |
| `multi-select` | `value: string[]`, `options` |
| `color` | `value: string`, optional `alpha` |
| `button` | optional `buttonLabel` |
| `date`, `time` | `value: string`; date may include `min` and `max` |
| `range` | `value: [number, number]`, `min`, `max`, optional `step` |
| `file`, `directory` | optional `value`; file may include `accept: string[]` |
| `info` | `text: string` |
| `link` | `url: string`, optional `linkLabel` |

Sections may also contain a `divider` item or a `header` item with a `label` and optional `description`.

```ts
SpotifyPlus.Settings.registerSetting({
  title: 'My extension',
  items: [
    { 
      id: 'enabled', 
      type: 'toggle', 
      label: 'Enabled', 
      value: true 
    },
    { 
      id: 'volume', 
      type: 'slider', 
      label: 'Volume', 
      value: 50, 
      min: 0, 
      max: 100 
    }
  ]
});
```
