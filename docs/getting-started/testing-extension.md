---
sidebar_label: 'Testing Your Extension'
sidebar_position: 1
---

Obviously when you're creating your extension, you're going to need to test it! Spotify Plus makes this very easy to do.

# Testing Your Extension

To begin, you will need to enable developer mode inside of Spotify. To do this, go to Spotify on your phone. Open the Spotify Plus settings, and go to developer settings. From here, you can enable developer mode. 

You can install your extension locally here by sending it to your device. However, that is slow and annoying. Spotify Plus allows you to hot reload your extension. To do this, you must plug your phone into your computer. Or, you can optionally use wireless debugging. If you decide to plug it in over USB, make sure to allow deubgging. You also need adb installed on your computer. You can install it from Google, and add it to your PATH.

Once you have your device plugged in, you can run `npm run dev` and it should send your extension to your phone! You will get all device logs in your console, and it will automatically update every time you edit your files. Once you are ready to build your extension, you can run `npm run build`.

:::note
Hot reload is currently not supported with native code. If you modify your Java/Kotlin code, you will have to rebuild your extension and reload it. 
:::