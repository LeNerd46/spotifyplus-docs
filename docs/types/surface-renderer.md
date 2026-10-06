---
sidebar_label: 'SurfaceRenderer'
---

# SurfaceRenderer

A renderer returns a React element for a scripted surface.

```ts
type SurfaceRenderer<T extends string = string> = (surface: { id: string; type: T }) => React.ReactElement;
```

```tsx
SpotifyPlus.Surfaces.register('lyrics-view', surface => (
  <Text>Surface {surface.id}</Text>
));
```
