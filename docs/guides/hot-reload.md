---
sidebar_position: 1
sidebar_label: 'Hot Reload'
---

# Hot Reload for Extensions

Yeah, having to build your extension, send it to your phone, and move it to the right location every time to test a simple change would be quite annoying. Don't worry, Spotify Plus supports hot reloading! Whenever you're developing your extension, just run `npx run dev`, and it will automatically send your extension to your phone, and any time you make a change, it will automatically reload your extension. Any assets you add will also be hot reloaded, as long as they are less than 25 MB. If it is more than 25 MB, you will have to rebuild and send your extension over to your phone.

## Getting Hot Reloading Working

There are a few steps you must take before hot reloading will work. Don't worry though! You might already have a lot of this done already. First, make sure you have developer mode enabled in Spotify Plus. Go to Spotify Plus Settings -> Developer -> Enable developer mode. 

Next, make sure you have adb installed. This is pretty simple, just look up the download link or whatever. You know how to install things on your computer. Then, you have to connect your phone to your computer. If you are using an emulator, you can skip this step. If you are using your real phone, make sure you have developer mode enabled on your phone, and debugging is enabled. If you plug your phone into your computer with a USB cable, it will ask you on your phone if you want to allow USB debugging. Please allow this. If you want to do it wirelessly, enable wireless debugging and pair your phone to your computer. If you need help with this, please see [this](https://medium.com/fludev/enable-wireless-debugging-in-android-ditch-the-usb-cable-74575d0da2f7) article.

You should be all set then! Run `npx run dev` with your device connected, and you should see your extension show up!