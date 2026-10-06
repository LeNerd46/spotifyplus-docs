---
sidebar_label: 'Extension assets'
---

# Extension assets

Asset methods return references to files bundled with the extension. The files must be declared in `manifest.assets`.

## ExtensionAsset

```ts
interface ExtensionAsset {
  readonly type: 'extension-asset';
  readonly uri: string;
  readonly mimeType: string;
  readonly name: string;
}
```

## ExtensionFontAsset

```ts
interface ExtensionFontAsset extends ExtensionAsset {
  readonly assetKind: 'font';
}
```

## ExtensionFontFace

```ts
interface ExtensionFontFace {
  source: string;
  weight?: 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;
  style?: 'normal' | 'italic';
}
```

## ExtensionFontFamily

```ts
interface ExtensionFontFamily {
  readonly type: 'extension-font-family';
  readonly faces: ReadonlyArray<{
    readonly source: ExtensionFontAsset;
    readonly weight: number;
    readonly style: 'normal' | 'italic';
  }>;
}
```