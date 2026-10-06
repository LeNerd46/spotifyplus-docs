---
sidebar_label: 'UI target types'
---

# UI target types

Import these types from `spotifyplus`. React component types refer to React. Named targets and selector shapes describe the public contract; check [current adapter support](../spotifyplus-api/ui/index.md#supported-boundaries) at runtime.

## UITargetName

```ts
type UITargetName =
    | 'home.page' | 'home.header' | 'home.section' | 'home.item'
    | 'search.page' | 'search.field' | 'search.filters' | 'search.results' | 'search.item'
    | 'library.page' | 'library.header' | 'library.filters' | 'library.list' | 'library.item'
    | `${'playlist' | 'album' | 'artist'}.${'page' | 'header' | 'actions' | 'section' | 'list' | 'item'}`
    | 'artist.discography.page' | 'settings.page' | 'profile.page'
    | `nowPlaying.${'page' | 'header' | 'artwork' | 'trackInfo' | 'controls' | 'seekBar' | 'card'}`
    | `miniPlayer.${'root' | 'artwork' | 'trackInfo' | 'controls'}`
    | `queue.${'page' | 'header' | 'content' | 'item'}`
    | `lyrics.${'page' | 'header' | 'content' | 'line'}`
    | `contextMenu.${'root' | 'header' | 'actions' | 'action'}`
    | 'navigation.bar' | 'navigation.item' | 'navigation.drawer'
    | `${string}:${string}`;
```

## UITarget

```ts
type UIOperation = 'replace' | 'before' | 'after' | 'overlay';
type UISelector = { screen: UITargetName } & (
    { resourceId: string; composeTag?: never } | { composeTag: string; resourceId?: never }
);
type UITarget = UITargetName | UISelector;
```

## UIPart

```ts
interface UIPart {
    readonly id: string;
    readonly semanticId: string;
    readonly kind: 'action' | 'content';
    readonly title: string | null;
    readonly enabled: boolean;
}
```

## UIInstance

```ts
interface UIInstance {
    readonly target: string;
    readonly context: UITargetContext;
}
```

## UITargetContext

```ts
interface UITargetContext {
    readonly instanceId: string;
    readonly uri: string | null;
    readonly pageUri: string | null;
    readonly title?: string | null;
    readonly subtitle?: string | null;
    readonly actionId?: string;
    readonly enabled?: boolean;
    /** Native menu actions/drawer rows, including content regions such as messaging. */
    readonly parts?: readonly UIPart[];
}
```

## UIComponentProps

```ts
interface UIComponentProps {
    readonly context: UITargetContext;
    /** Mount once, within a replacement of this target. Native interaction remains native. */
    readonly Original: React.ComponentType;
    /** Render a listed part with Spotify's live renderer, preserving its native behavior. */
    readonly NativePart: React.ComponentType<{ id: string }>;
}
```

## UIRegistration

```ts
interface UIRegistration {
    readonly id: string;
    dispose(): void;
}
```

## UITargetInfo

```ts
interface UITargetInfo {
    name: string;
    available: boolean;
    operations: UIOperation[];
    reason?: string;
    instances: number;
    conflicts: Array<{ instanceId: string; winner: string; suppressed: string[] }>;
}
```

`instanceId` and part `id` belong to a live target instance. Do not persist them or reuse them after a model refresh. `semanticId` describes the native action/destination/content; `title` is localized and nullable. `parts` is supplied by drawer/menu roots. Context changes update a mounted component without replacing its React state.

`available` describes adapter support, while `instances` counts currently mounted boundaries. An available screen can have zero instances. `Original` is valid only in replacements; `NativePart` must reference a current part of its own instance.
