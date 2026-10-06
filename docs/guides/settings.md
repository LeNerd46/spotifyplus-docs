---
sidebar_position: 0
sidebar_label: 'Extension Settings'
---

# Giving Your Extension Settings

Many extensoins may want to have settings to allow the user to change your extension to their liking. Spotify Plus allows a easy to use and unified place for extensions to register all of their settings. You are by no means required to use this. If you have a better place for your extension's settings, go ahead. This is just so that each extension doesn't flood the side drawer with settings buttons. 

## Understanding Settings

Spotify Plus separates settings into sections. Sections are just related settings grouped under a common title. For example, you might have a general section with miscellaneous settings. You might have another section titled visuals with a bunch of settings related to changing the visuals of something. That is what sections are.

Sections have a title, an optional description, and a list of settings. You are able to have dividers and headings as well, if you need to split sections up into subcategories. 

## Registering Settings

In order for your settings to show up, you have to register them. Luckily, regisering your settings is super easy! You can either register them one section at a time, or you can register them all at once. 

This is an example of registerring one section.

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

This is an example of registering them all at once. It also includes headers and dividers

```ts
SpotifyPlus.Settings.registerSettings([
    {
        title: 'General',
        items: [
            {
                type: 'toggle',
                id: 'enabled',
                label: 'Enabled',
                value: true
            }
        ]
    },
    {
        title: 'Display',
        items: [
            {
                type: 'text',
                id: 'greeting',
                label: 'Greeting',
                value: 'Hello'
            },
            {
                type: 'divider'
            },
            {
                type: 'header',
                label: 'The content of the header',
                description: 'This is to show how to create headers'
            },
            {
                type: 'button',
                id: 'button-thing',
                label: 'This is a really cool button',
                description: "Press this button and you'll be really cool"
            }
        ]
    },
]);
```

You should register this in your entry file so that it will show up as early as possible. 