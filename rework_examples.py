from pathlib import Path
import re

ROOT = Path(__file__).parent / 'docs' / 'spotifyplus-api'

# Each example deliberately shows where values come from and checks optional results.
EXAMPLES = {
    'search/search': '''// Find albums that match the user's search.
const results = await SpotifyPlus.Search.search('After Hours', { limit: 20 });

// Search contains several item kinds, so select an album.
const album = results.items.find(item => item.uri.startsWith('spotify:album:'));
if (!album) return;

// Open the album page inside Spotify.
SpotifyPlus.Navigation.openSpotify(album.uri);''',
    'connect/get-devices': '''// Find devices that can receive playback.
const devices = await SpotifyPlus.Connect.getDevices();
const available = devices.filter(device => !device.isDisabled);

for (const device of available) {
  SpotifyPlus.log(`${device.name}: ${device.isActive ? 'active' : 'available'}`);
}


if (available.length === 0) SpotifyPlus.toast('No Connect devices found');''',
    'connect/get-current-device': '''// Show the device currently playing music.
const device = await SpotifyPlus.Connect.getCurrentDevice();
if (!device) {
  SpotifyPlus.toast('No active playback device');
  return;
}

SpotifyPlus.toast(`Playing on ${device.name}`);
SpotifyPlus.log('Raw volume:', device.volume);''',
    'connect/transfer': '''// Prefer another available device over the current one.
const devices = await SpotifyPlus.Connect.getDevices();
const target = devices.find(device => !device.isActive && !device.isDisabled);
if (!target) {
  SpotifyPlus.toast('No other device is available');
  return;
}

await SpotifyPlus.Connect.transfer(target);
SpotifyPlus.toast(`Transferred playback to ${target.name}`);''',
    'playlists/get': '''// Get the first playlist saved in the user's library.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 1 });
const playlistUri = saved.items[0]?.uri;
if (!playlistUri) return;

// Read its first page of tracks and its total track count.
const playlist = await SpotifyPlus.Playlists.get(playlistUri, { offset: 0, limit: 25 });
SpotifyPlus.log(`${playlist.name} has ${playlist.total} tracks`);
for (const item of playlist.items) SpotifyPlus.log(item.name);''',
    'playlists/create': '''// Make a new playlist, then put a track into it.
const playlist = await SpotifyPlus.Playlists.create('Songs to revisit');
const track = SpotifyPlus.Player.getCurrentTrack();

if (track.uri) {
  await SpotifyPlus.Playlists.addTracks(playlist.uri, [track.uri]);
}

SpotifyPlus.toast(`Created ${playlist.name}`);''',
    'playlists/delete': '''// Select a playlist that belongs to the current user.
const saved = await SpotifyPlus.Library.list({ type: 'playlist' });
const owned = await Promise.all(saved.items.map(item => SpotifyPlus.Playlists.get(item.uri)));
const playlist = owned.find(item => item.ownedBySelf && item.name === 'Songs to revisit');
if (!playlist) return;

// This removes the playlist from the user's library.
await SpotifyPlus.Playlists.delete(playlist.uri);
SpotifyPlus.toast('Playlist removed');''',
    'playlists/move': '''// Move the second saved playlist ahead of the first.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 2 });
if (saved.items.length < 2) return;

const first = saved.items[0];
const second = saved.items[1];
await SpotifyPlus.Playlists.move(second.uri, first.uri);
SpotifyPlus.toast(`${second.name} moved to the top`);''',
    'playlists/add-tracks': '''// Add the current track to the user's first saved playlist.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 1 });
const playlist = saved.items[0];
if (!playlist) return;

const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

await SpotifyPlus.Playlists.addTracks(playlist.uri, [track.uri]);
SpotifyPlus.toast(`Added to ${playlist.name}`);''',
    'playlists/remove-tracks': '''// Read a playlist so we can target one exact row.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 1 });
const playlistUri = saved.items[0]?.uri;
if (!playlistUri) return;

const page = await SpotifyPlus.Playlists.get(playlistUri, { limit: 20 });
const duplicate = page.items.find(item => item.uri === page.items[0]?.uri);
if (!duplicate) return;

// A row ID removes this occurrence, even if the track appears elsewhere.
await SpotifyPlus.Playlists.removeTracks(playlistUri, [duplicate.rowId]);''',
    'playlists/move-tracks': '''// Put the second track before the first track in a playlist.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 1 });
const playlistUri = saved.items[0]?.uri;
if (!playlistUri) return;

const page = await SpotifyPlus.Playlists.get(playlistUri, { limit: 2 });
if (page.items.length < 2) return;

await SpotifyPlus.Playlists.moveTracks(
  playlistUri, [page.items[1].rowId], page.items[0].rowId
);''',
    'user/get-current': '''// Greet the signed-in user by their display name.
const user = await SpotifyPlus.User.getCurrent();
const name = user.displayName || user.username;

SpotifyPlus.toast(`Welcome, ${name}`);
SpotifyPlus.log('Profile URI:', user.uri);
if (user.images.length) SpotifyPlus.log('Avatar:', user.images[0].url);''',
    'library/list': '''// Read the first page of saved albums.
const page = await SpotifyPlus.Library.list({ type: 'album', offset: 0, limit: 20 });
SpotifyPlus.log(`You have ${page.total} saved albums`);

for (const album of page.items) {
  SpotifyPlus.log(album.name, album.uri);
}

// Request the next page when more results remain.
if (page.offset + page.items.length < page.total) {
  const next = await SpotifyPlus.Library.list({ type: 'album', offset: 20, limit: 20 });
  SpotifyPlus.log('Next page:', next.items.length);
}''',
    'library/save': '''// Find an album, then save it to the user's library.
const results = await SpotifyPlus.Search.search('After Hours');
const album = results.items.find(item => item.uri.startsWith('spotify:album:'));
if (!album) return;

await SpotifyPlus.Library.save(album.uri);
SpotifyPlus.toast(`Saved ${album.text}`);''',
    'library/remove': '''// Find a saved album by its name.
const page = await SpotifyPlus.Library.list({ type: 'album' });
const album = page.items.find(item => item.name === 'After Hours');
if (!album) return;

await SpotifyPlus.Library.remove(album.uri);
SpotifyPlus.toast(`Removed ${album.name} from your library`);''',
    'library/contains': '''// Check several search results before showing Save actions.
const results = await SpotifyPlus.Search.search('After Hours');
const albums = results.items.filter(item => item.uri.startsWith('spotify:album:'));
if (albums.length === 0) return;

const saved = await SpotifyPlus.Library.contains(albums.map(album => album.uri));
albums.forEach((album, index) => {
  SpotifyPlus.log(album.text, saved[index] ? 'saved' : 'not saved');
});''',
    'library/like': '''// Like the song currently playing, if it is not already liked.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

if (!(await SpotifyPlus.Library.isLiked(track.uri))) {
  await SpotifyPlus.Library.like(track.uri);
  SpotifyPlus.toast(`Liked ${track.title}`);
}''',
    'library/unlike': '''// Remove the current song from Liked Songs.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

if (await SpotifyPlus.Library.isLiked(track.uri)) {
  await SpotifyPlus.Library.unlike(track.uri);
  SpotifyPlus.toast(`Unliked ${track.title}`);
}''',
    'library/is-liked': '''// Show whether the current track is in Liked Songs.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

const liked = await SpotifyPlus.Library.isLiked(track.uri);
SpotifyPlus.toast(liked ? 'Already in Liked Songs' : 'Not yet liked');''',
    'queue/get': '''// Display the next three tracks in the playback queue.
const snapshot = await SpotifyPlus.Queue.get();
SpotifyPlus.log('Now playing:', snapshot.current?.uri ?? 'nothing');

for (const [index, entry] of snapshot.next.slice(0, 3).entries()) {
  SpotifyPlus.log(`${index + 1}. ${entry.uri}`);
}

SpotifyPlus.log('Queue revision:', snapshot.revision);''',
    'queue/add': '''// Find a track and put it at the end of the queue.
const results = await SpotifyPlus.Search.search('Blinding Lights');
const track = results.items.find(item => item.uri.startsWith('spotify:track:'));
if (!track) return;

await SpotifyPlus.Queue.add(track.uri);
SpotifyPlus.toast(`Queued ${track.text}`);''',
    'queue/remove': '''// Remove the next queued occurrence without affecting the current song.
const snapshot = await SpotifyPlus.Queue.get();
const next = snapshot.next[0];
if (!next) return;

try {
  await SpotifyPlus.Queue.remove(snapshot, 0);
  SpotifyPlus.toast('Removed from queue');
} catch (error) {
  // The queue may have changed since this snapshot was read.
  SpotifyPlus.warn('Queue changed; fetch it again', error);
}''',
    'queue/move': '''// Make the second upcoming song play next.
const snapshot = await SpotifyPlus.Queue.get();
if (snapshot.next.length < 2) return;

try {
  await SpotifyPlus.Queue.move(snapshot, 1, 0);
  SpotifyPlus.toast('Moved song to the front of the queue');
} catch (error) {
  // Get a fresh snapshot before trying another reorder.
  SpotifyPlus.warn('Queue changed', error);
}''',
    'queue/clear': '''// Clear upcoming songs while leaving the current track alone.
const snapshot = await SpotifyPlus.Queue.get();
if (snapshot.next.length === 0) return;

await SpotifyPlus.Queue.clear(snapshot);
SpotifyPlus.toast(`Cleared ${snapshot.next.length} upcoming songs`);''',
    'navigation/open': '''// Open an album inside Spotify if search finds one.
const results = await SpotifyPlus.Search.search('After Hours');
const album = results.items.find(item => item.uri.startsWith('spotify:album:'));
if (!album) return;

const opened = SpotifyPlus.Navigation.open(album.uri, { target: 'spotify' });
if (!opened) SpotifyPlus.toast('Could not open the album');''',
    'navigation/open-spotify': '''// Open the current track's page inside Spotify.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

const opened = SpotifyPlus.Navigation.openSpotify(track.uri);
if (!opened) SpotifyPlus.warn('Spotify did not open the track page');''',
    'navigation/open-external': '''// Send the user to a help page in their browser.
const helpUrl = 'https://www.spotify.com/';
const opened = SpotifyPlus.Navigation.openExternal(helpUrl);

if (!opened) {
  SpotifyPlus.toast('Could not open the browser');
}''',
    'navigation/back': '''// Return from a page opened by the extension.
SpotifyPlus.Navigation.openSpotify('spotify:album:4aawyAB9vmqN3uQ7FjRGTy');

// Later, after the user is done with that page:
const handled = SpotifyPlus.Navigation.back();
if (!handled) SpotifyPlus.log('There is no Spotify page to return to');''',
    'platform/clipboard/read-text': '''// Look for a Spotify track URI copied by the user.
const text = await SpotifyPlus.Platform.Clipboard.readText();
if (!text?.startsWith('spotify:track:')) {
  SpotifyPlus.toast('Copy a Spotify track URI first');
  return;
}

const track = await SpotifyPlus.Internal.getTrack(text);
if (track) SpotifyPlus.toast(`Copied track: ${track.title}`);''',
    'platform/clipboard/write-text': '''// Let the user copy the URI of the current song.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

await SpotifyPlus.Platform.Clipboard.writeText(track.uri);
SpotifyPlus.toast('Track URI copied');''',
    'platform/clipboard/clear': '''// Clear a URI the extension just placed on the clipboard.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

await SpotifyPlus.Platform.Clipboard.writeText(track.uri);
// After the user finishes sharing it:
await SpotifyPlus.Platform.Clipboard.clear();''',
    'platform/storage/set': '''// Save a user preference when they enable a feature.
const enabled = true;
SpotifyPlus.Platform.Storage.set('showTrackToasts', enabled);

// The preference is scoped to this extension.
SpotifyPlus.log('Track toasts enabled:', enabled);''',
    'platform/storage/get': '''// Restore a preference, choosing a default the first time.
const saved = await SpotifyPlus.Platform.Storage.get<boolean>('showTrackToasts');
const enabled = saved ?? true;

if (enabled) {
  const track = SpotifyPlus.Player.getCurrentTrack();
  SpotifyPlus.toast(`Now playing: ${track.title}`);
}''',
    'platform/storage/remove': '''// Reset a preference to its default value.
const key = 'showTrackToasts';
const oldValue = await SpotifyPlus.Platform.Storage.get<boolean>(key);
if (oldValue !== null) {
  SpotifyPlus.Platform.Storage.remove(key);
  SpotifyPlus.toast('Preference reset');
}''',
    'platform/storage/write': '''// Persist a larger object in an extension-owned file.
const current = SpotifyPlus.Player.getCurrentTrack();
const lastPlayed = {
  uri: current.uri,
  title: current.title,
  savedAt: Date.now(),
};

SpotifyPlus.Platform.Storage.write('history/last-played.json', lastPlayed);''',
    'platform/storage/read': '''// Restore the last track recorded by this extension.
type LastPlayed = { uri: string; title: string; savedAt: number };
const value = await SpotifyPlus.Platform.Storage.read<LastPlayed>('history/last-played.json');

if (value && typeof value !== 'string' && !(value instanceof Uint8Array)) {
  SpotifyPlus.log(`Last played: ${value.title}`);
  SpotifyPlus.Navigation.openSpotify(value.uri);
}''',
    'platform/storage/delete': '''// Remove a file when the user clears their history.
const path = 'history/last-played.json';
const previous = await SpotifyPlus.Platform.Storage.read(path);
if (previous !== null) {
  SpotifyPlus.Platform.Storage.delete(path);
  SpotifyPlus.toast('Playback history cleared');
}''',
    'platform/storage/cache/write': '''// Cache a search response for this extension.
const query = 'After Hours';
const results = await SpotifyPlus.Search.search(query);

SpotifyPlus.Platform.Storage.Cache.write('search/after-hours.json', {
  query,
  items: results.items,
});
SpotifyPlus.log(`Cached ${results.items.length} results`);''',
    'platform/storage/cache/read': '''// Use a recent cached search if Android has kept it.
type CachedSearch = { query: string; items: Array<{ uri: string; text: string }> };
const cached = await SpotifyPlus.Platform.Storage.Cache.read<CachedSearch>('search/after-hours.json');

if (cached && typeof cached !== 'string' && !(cached instanceof Uint8Array)) {
  SpotifyPlus.log(`Cached results for ${cached.query}:`, cached.items.length);
} else {
  SpotifyPlus.log('Cache miss; run Search.search() again');
}''',
    'platform/storage/cache/delete': '''// Discard old search results after a fresh search.
const results = await SpotifyPlus.Search.search('After Hours');
if (results.items.length > 0) {
  SpotifyPlus.Platform.Storage.Cache.delete('search/after-hours.json');
  SpotifyPlus.log('Removed stale search cache');
}''',
    'internal/get-track': '''// Fetch full metadata for the currently playing song.
const current = SpotifyPlus.Player.getCurrentTrack();
if (!current.uri) return;

const track = await SpotifyPlus.Internal.getTrack(current.uri);
if (!track) return;

SpotifyPlus.log(`${track.title} by ${track.artists.join(', ')}`);
SpotifyPlus.log('Explicit:', track.explicit);''',
    'internal/get-album': '''// Search for an album, then list its first disc's track URIs.
const results = await SpotifyPlus.Search.search('After Hours');
const match = results.items.find(item => item.uri.startsWith('spotify:album:'));
if (!match) return;

const album = await SpotifyPlus.Internal.getAlbum(match.uri);
if (!album) return;

SpotifyPlus.log(`${album.name} by ${album.artists.map(a => a.name).join(', ')}`);
for (const uri of album.discs[0]?.tracks ?? []) SpotifyPlus.log(uri);''',
    'internal/get-artist': '''// Search for an artist, then show their top tracks.
const results = await SpotifyPlus.Search.search('Taylor Swift');
const match = results.items.find(item => item.uri.startsWith('spotify:artist:'));
if (!match) return;

const artist = await SpotifyPlus.Internal.getArtist(match.uri);
if (!artist) return;

SpotifyPlus.log(artist.name);
for (const uri of artist.topTracks[0]?.tracks ?? []) SpotifyPlus.log(uri);''',
    'internal/get-playlist': '''// Read playlist metadata without fetching a paginated track page.
const saved = await SpotifyPlus.Library.list({ type: 'playlist', limit: 1 });
const uri = saved.items[0]?.uri;
if (!uri) return;

const playlist = await SpotifyPlus.Internal.getPlaylist(uri);
if (!playlist) return;

SpotifyPlus.log(`${playlist.name}: ${playlist.length} tracks`);
SpotifyPlus.log('Can edit items:', playlist.canEditItems);''',
    'player/get-progress': '''// Show a rounded elapsed time for the current track.
const track = SpotifyPlus.Player.getCurrentTrack();
const positionMs = SpotifyPlus.Player.getProgress();

const elapsed = Math.floor(positionMs / 1000);
const duration = Math.floor(track.durationMs / 1000);
SpotifyPlus.log(`${elapsed}s of ${duration}s: ${track.title}`);''',
    'player/play': '''// Resume playback only when Spotify is paused.
const state = await SpotifyPlus.Player.getState();
if (!state.isPaused) return;

await SpotifyPlus.Player.play();
SpotifyPlus.toast('Playback resumed');''',
    'player/pause': '''// Pause only if a track is currently playing.
const state = await SpotifyPlus.Player.getState();
if (!state.isPlaying) return;

await SpotifyPlus.Player.pause();
SpotifyPlus.toast('Playback paused');''',
    'player/toggle-play': '''// Use the current state to label a play/pause action.
const before = await SpotifyPlus.Player.getState();
await SpotifyPlus.Player.togglePlay();

SpotifyPlus.toast(before.isPlaying ? 'Paused' : 'Playing');''',
    'player/skip-next': '''// Skip ahead only if a song is already in the queue.
const queue = await SpotifyPlus.Queue.get();
if (queue.next.length === 0) {
  SpotifyPlus.toast('Nothing is queued next');
  return;
}

await SpotifyPlus.Player.skipNext();
SpotifyPlus.toast('Skipped to the next song');''',
    'player/skip-previous': '''// Return to the start of the current song, or go to the previous one.
const state = await SpotifyPlus.Player.getState();
if (!state.trackUri) return;

await SpotifyPlus.Player.skipPrevious();
const updated = await SpotifyPlus.Player.getState();
SpotifyPlus.log('Now playing:', updated.trackUri);''',
    'surfaces/register': '''// Render the extension's lyrics panel when that surface opens.
function MyLyricsPanel() {
  const track = SpotifyPlus.Player.getCurrentTrack();
  return <Text>{track.title}</Text>;
}

SpotifyPlus.Surfaces.register('lyrics-view', () => <MyLyricsPanel />);''',
    'surfaces/close': '''// Close a scripted view after the user completes an action.
const track = SpotifyPlus.Player.getCurrentTrack();
if (track.uri) {
  await SpotifyPlus.Platform.Clipboard.writeText(track.uri);
  SpotifyPlus.toast('Track URI copied');
}

const closed = SpotifyPlus.Surfaces.close();
if (!closed) SpotifyPlus.log('No scripted view was open');''',
    'settings/test': '''// Send a message while developing a settings screen.
SpotifyPlus.Settings.test('Settings registration started');

SpotifyPlus.Settings.registerSetting({
  title: 'General',
  items: [{ type: 'toggle', id: 'enabled', label: 'Enabled', value: true }],
});

SpotifyPlus.Settings.test('Settings registration complete');''',
    'settings/register-setting': '''// Build one settings section for playback behavior.
const section = {
  title: 'Playback',
  description: 'Choose how this extension responds to songs.',
  items: [
    { type: 'toggle' as const, id: 'showToast', label: 'Show track toast', value: true },
    { type: 'slider' as const, id: 'delay', label: 'Toast delay', value: 2, min: 0, max: 10 },
  ],
};

SpotifyPlus.Settings.registerSetting(section);''',
    'settings/register-settings': '''// Register separate sections for general and display preferences.
SpotifyPlus.Settings.registerSettings([
  {
    title: 'General',
    items: [{ type: 'toggle', id: 'enabled', label: 'Enabled', value: true }],
  },
  {
    title: 'Display',
    items: [{ type: 'text', id: 'greeting', label: 'Greeting', value: 'Hello' }],
  },
]);''',
    'events/on': '''// Update a stored URI whenever Spotify changes songs.
const onSongChanged = ({ uri }: { uri: string | null }) => {
  if (!uri) return;
  SpotifyPlus.Platform.Storage.set('lastTrackUri', uri);
  SpotifyPlus.log('New track:', uri);
};

SpotifyPlus.Events.on('songChanged', onSongChanged);
// Keep the same function reference if you later call Events.off().''',
    'events/once': '''// Greet the user only on the next song change.
SpotifyPlus.Events.once('songChanged', async ({ uri }) => {
  if (!uri) return;
  const track = await SpotifyPlus.Internal.getTrack(uri);
  if (track) SpotifyPlus.toast(`Now playing: ${track.title}`);
});

// The listener removes itself after that event.''',
    'events/off': '''// Subscribe while a feature is enabled, then remove the listener.
const onShuffleChanged = ({ enabled }: { enabled: boolean }) => {
  SpotifyPlus.log(enabled ? 'Shuffle on' : 'Shuffle off');
};

SpotifyPlus.Events.on('shuffleChanged', onShuffleChanged);
// When the feature is turned off:
SpotifyPlus.Events.off('shuffleChanged', onShuffleChanged);''',
    'events/emit': '''// Announce that this extension opened a panel.
SpotifyPlus.Events.on('panelOpened', ({ source }: { source: string }) => {
  SpotifyPlus.log('Panel opened from', source);
});

await SpotifyPlus.Events.emit('panelOpened', { source: 'side drawer' });
// Custom events stay in this extension.''',
    'assets/resolve': '''// Resolve a declared audio file for use elsewhere in the extension.
const alert = SpotifyPlus.Assets.resolve('sounds/alert.mp3');

SpotifyPlus.log(alert.name);
SpotifyPlus.log(alert.mimeType);
SpotifyPlus.log('Asset URI:', alert.uri);''',
    'assets/image': '''// Resolve a declared icon and use it in the side drawer.
const icon = SpotifyPlus.Assets.image('images/heart.png');

new SpotifyPlus.SideDrawer(
  'Liked Songs helper',
  () => <LikedSongsPanel />,
  icon
).register();''',
    'assets/font': '''// Resolve a custom font declared in manifest.assets.
const font = SpotifyPlus.Assets.font('fonts/Brand.ttf');

SpotifyPlus.log('Loaded font:', font.name);
SpotifyPlus.log('MIME type:', font.mimeType);
// Pass this asset to code that accepts an ExtensionFontAsset.''',
    'assets/font-family': '''// Combine regular and bold font files into one family.
const family = SpotifyPlus.Assets.fontFamily([
  { source: 'fonts/Brand-Regular.ttf', weight: 400 },
  { source: 'fonts/Brand-Bold.ttf', weight: 700 },
]);

SpotifyPlus.log('Available font faces:', family.faces.length);
// Use the family in a component style that accepts custom fonts.''',
    'assets/read-text': '''// Show text from a file bundled with the extension.
const license = SpotifyPlus.Assets.readText('data/license.txt');
const firstLine = license.split('\n')[0];

SpotifyPlus.log('License:', firstLine);
SpotifyPlus.toast('License loaded');''',
    'assets/read-json': '''// Read bundled defaults and use them for an extension preference.
type Defaults = { showTrackToasts: boolean };
const defaults = SpotifyPlus.Assets.readJson<Defaults>('data/defaults.json');

const saved = await SpotifyPlus.Platform.Storage.get<boolean>('showTrackToasts');
const enabled = saved ?? defaults.showTrackToasts;
SpotifyPlus.log('Track toasts enabled:', enabled);''',
    'assets/read-bytes': '''// Inspect a binary file bundled with the extension.
const bytes = SpotifyPlus.Assets.readBytes('sounds/alert.mp3');
if (bytes.length === 0) {
  SpotifyPlus.warn('The alert sound is empty');
  return;
}

SpotifyPlus.log(`Loaded ${bytes.length} audio bytes`);''',
    'ui/replace': '''// Replace a supported header with a component that keeps the native view.
function Header({ context, Original }: UIComponentProps) {
  return <><Original /><Text>{context.title}</Text></>;
}

const info = await SpotifyPlus.UI.inspect('nowPlaying.header');
if (!info.available || !info.operations.includes('replace')) return;

const registration = SpotifyPlus.UI.replace('nowPlaying.header', Header);
// Call registration.dispose() when this UI is no longer needed.''',
    'ui/insert-before': '''// Add a banner before the first supported home section.
function Banner() { return <Text>Welcome back!</Text>; }

const info = await SpotifyPlus.UI.inspect('home.section');
if (!info.available || !info.operations.includes('before')) return;

const registration = SpotifyPlus.UI.insertBefore('home.section', Banner);
// Remove it later with registration.dispose().''',
    'ui/insert-after': '''// Show an extra note below a supported home section.
function Note() { return <Text>Made with Spotify Plus</Text>; }

const info = await SpotifyPlus.UI.inspect('home.section');
if (!info.available || !info.operations.includes('after')) return;

const registration = SpotifyPlus.UI.insertAfter('home.section', Note);
// Remove it later with registration.dispose().''',
    'ui/overlay': '''// Place a small status label over the now-playing artwork.
function Status() { return <Text>Live</Text>; }

const info = await SpotifyPlus.UI.inspect('nowPlaying.artwork');
if (!info.available || !info.operations.includes('overlay')) return;

const registration = SpotifyPlus.UI.overlay('nowPlaying.artwork', Status);
// Dispose the registration when the overlay is no longer needed.''',
    'ui/inspect': '''// Check what the installed Spotify build supports.
const info = await SpotifyPlus.UI.inspect('nowPlaying.header');
if (!info.available) {
  SpotifyPlus.warn(info.reason ?? 'Header target unavailable');
  return;
}

SpotifyPlus.log('Supported operations:', info.operations);
SpotifyPlus.log('Active instances:', info.instances);''',
    'ui/list-targets': '''// Find targets that can be replaced on this Spotify build.
const targets = await SpotifyPlus.UI.listTargets();
const replaceable = targets.filter(target =>
  target.available && target.operations.includes('replace')
);

for (const target of replaceable) SpotifyPlus.log(target.name);
SpotifyPlus.toast(`${replaceable.length} replacement targets available`);''',
    'api/log': '''// Record the current track during extension startup.
SpotifyPlus.log('Starting extension', SpotifyPlus.scriptId);

const state = await SpotifyPlus.Player.getState();
SpotifyPlus.log('Current track URI:', state.trackUri);
SpotifyPlus.log('Playback position:', state.positionMs);''',
    'api/warn': '''// Explain why an optional feature cannot run yet.
const device = await SpotifyPlus.Connect.getCurrentDevice();
if (!device) {
  SpotifyPlus.warn('No active Connect device; transfer action is unavailable');
  return;
}

SpotifyPlus.log('Active device:', device.name);''',
    'api/error': '''// Log an unexpected playback failure with context.
try {
  await SpotifyPlus.Player.play();
} catch (error) {
  SpotifyPlus.error('Could not resume playback', error);
  SpotifyPlus.toast('Playback could not be resumed');
}''',
    'api/on': '''// Keep a scripted surface open when Android Back is pressed.
const handleBack = (event: { preventDefault(): void }) => {
  event.preventDefault();
  SpotifyPlus.Navigation.back();
};

SpotifyPlus.on('android.backPressed', handleBack);
// Remove the handler with SpotifyPlus.off() when finished.''',
    'api/off': '''// Stop handling Android Back after closing a custom view.
const handleBack = (event: { preventDefault(): void }) => event.preventDefault();
SpotifyPlus.on('android.backPressed', handleBack);

SpotifyPlus.Surfaces.close();
SpotifyPlus.off('android.backPressed', handleBack);''',
    'api/request': '''// Ask a host handler to perform an extension-specific operation.
type Result = { accepted: boolean };

try {
  const result = await SpotifyPlus.request<Result>('my.extension.command', { enabled: true });
  SpotifyPlus.log('Request accepted:', result.accepted);
} catch (error) {
  SpotifyPlus.error('Host request failed', error);
}''',
    'api/toast': '''// Confirm a successful action to the user.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

await SpotifyPlus.Library.like(track.uri);
SpotifyPlus.toast(`Liked ${track.title}`, 'short');''',
    'api/open-uri': '''// Open an album with the legacy navigation helper.
const results = await SpotifyPlus.Search.search('After Hours');
const album = results.items.find(item => item.uri.startsWith('spotify:album:'));
if (!album) return;

SpotifyPlus.openUri(album.uri);
// New code should use Navigation.open() for a success result.''',
    'api/emit': '''// Notify the host about an extension-specific action.
const track = SpotifyPlus.Player.getCurrentTrack();
if (!track.uri) return;

SpotifyPlus.emit('my.extension.trackSelected', { uri: track.uri });
SpotifyPlus.log('Sent track selection to host');''',
}

TYPE_LINKS = {
    'SpotifyUriInput': '/docs/types/spotify-uri-input',
    'RepeatMode': '/docs/types/repeat-mode',
    'PlaybackState': '/docs/types/playback-state',
    'SpotifyTrack': '/docs/types/spotify-track',
    'SearchOptions': '/docs/types/api-types#searchoptions',
    'SearchResponse': '/docs/types/api-types#searchresponse',
    'ConnectDevice': '/docs/types/api-types#connectdevice',
    'PlaylistPage': '/docs/types/api-types#playlistpage',
    'PageOptions': '/docs/types/api-types#pageoptions',
    'SpotifyUser': '/docs/types/api-types#spotifyuser',
    'QueueSnapshot': '/docs/types/api-types#queuesnapshot',
    'MetadataAlbum': '/docs/types/metadata#metadataalbum',
    'MetadataArtist': '/docs/types/metadata#metadataartist',
    'MetadataPlaylist': '/docs/types/metadata#metadataplaylist',
    'ExtensionAsset': '/docs/types/extension-assets#extensionasset',
    'ExtensionFontAsset': '/docs/types/extension-assets#extensionfontasset',
    'ExtensionFontFace': '/docs/types/extension-assets#extensionfontface',
    'ExtensionFontFamily': '/docs/types/extension-assets#extensionfontfamily',
    'UITarget': '/docs/types/ui-targets#uitarget',
    'UIComponentProps': '/docs/types/ui-targets#uicomponentprops',
    'UIRegistration': '/docs/types/ui-targets#uiregistration',
    'UITargetInfo': '/docs/types/ui-targets#uitargetinfo',
    'ExtensionSettingSection': '/docs/types/extension-settings#extensionsettingsection',
    'NavigationOptions': '/docs/types/navigation-options',
    'SurfaceRenderer': '/docs/types/surface-renderer',
    'ExtensionEventHandler': '/docs/types/event-handlers',
    'EventHandler': '/docs/types/event-handlers',
}

PARAMS = {
    'query': 'The words to search for.',
    'options': 'Optional settings for this request.',
    'device': 'The device ID or a device returned by `getDevices()`.',
    'playlist': 'The playlist to read or change.',
    'before': 'The playlist that should follow the moved playlist. Omit it to move to the beginning.',
    'tracks': 'The track URIs to add.',
    'rowIds': 'The IDs of individual playlist rows returned by `Playlists.get()`.',
    'beforeRowId': 'The row to place the selected rows before. Omit it to move them to the end.',
    'name': 'The name to use.',
    'items': 'One item or an array of items to process.',
    'track': 'The Spotify URI of the track.',
    'snapshot': 'A snapshot returned by `Queue.get()`, including its current revision.',
    'index': 'The zero-based position of the item.',
    'toIndex': 'The item’s final zero-based position in the upcoming queue.',
    'uri': 'The URI of the Spotify item.',
    'url': 'The HTTP or HTTPS URL to open.',
    'text': 'The text to use.',
    'key': 'The extension-scoped preference key.',
    'value': 'The value to store.',
    'path': 'A path relative to this extension’s storage area.',
    'relativePath': 'A path to a file declared in `manifest.assets`.',
    'faces': 'One or more bundled font face definitions.',
    'target': 'The named Spotify UI target or a target selector.',
    'component': 'The React component to mount at the target.',
    'surfaceType': 'The scripted surface type that triggers the renderer.',
    'renderer': 'The function that returns a React element for this surface.',
    'setting': 'A section containing settings items.',
    'settings': 'The sections to register.',
    'eventName': 'The event name to listen for or emit.',
    'handler': 'The callback to invoke for this event.',
    'payload': 'Optional data to send with the event or request.',
    'length': 'How long the toast should be visible. Defaults to `short`.',
    'enabled': 'Whether this feature should be enabled.',
    'message': 'The message to send to the settings host.',
    'args': 'The values to include in the log entry.',
}

PARAM_OVERRIDES = {
    'search/search': {'options': 'Optional `limit` and `locale` for the search.'},
    'playlists/get': {'options': 'Optional `offset` and `limit` for playlist pagination.'},
    'library/list': {'options': 'Optional `offset`, `limit`, and item `type` filter.'},
    'library/contains': {'items': 'The item URIs to check, in result order.'},
    'queue/add': {'items': 'One URI or an array of URIs to queue.'},
    'queue/remove': {'index': 'The zero-based index in `snapshot.next` to remove.'},
    'queue/move': {'index': 'The zero-based index in `snapshot.next` to move.'},
    'navigation/open': {'uri': 'The absolute URI to open.', 'options': 'Optional app target: `auto`, `spotify`, or `external`.'},
    'api/request': {'name': 'The name of a request handled by the host.'},
    'api/toast': {'text': 'The message to display.'},
    'api/open-uri': {'uri': 'The URI to open using automatic navigation.'},
    'assets/read-json': {'relativePath': 'The declared JSON file to parse.'},
    'events/off': {'handler': 'The exact callback reference previously passed to `Events.on()` or `Events.once()`.'},
    'api/off': {'handler': 'The exact callback reference previously passed to `SpotifyPlus.on()`.'},
}

def split_parameters(raw):
    if not raw.strip():
        return []
    parts, start = [], 0
    depth = 0
    for i, char in enumerate(raw):
        if char in '<{[(':
            depth += 1
        elif char in '>}])':
            depth -= 1
        elif char == ',' and depth == 0:
            parts.append(raw[start:i].strip())
            start = i + 1
    parts.append(raw[start:].strip())
    return parts

def linked_syntax(signature):
    from html import escape
    result = escape(signature, quote=False)
    for name, href in sorted(TYPE_LINKS.items(), key=lambda pair: -len(pair[0])):
        result = re.sub(rf'\b{name}\b', f'<a href="{href}">{name}</a>', result)
    return '<CodeBlock language="ts">\n  <span style={{ display: \'inline\' }}>' + result + '</span>\n</CodeBlock>'

def type_badge(type_name):
    from html import escape
    escaped = escape(type_name, quote=False)
    if type_name in TYPE_LINKS:
        return f'<Badge href="{TYPE_LINKS[type_name]}">{escaped}</Badge>'
    return f'<Badge>{escaped}</Badge>'

def rewrite(path):
    original = path.read_text(encoding='utf-8')
    relative = path.relative_to(ROOT).with_suffix('').as_posix()
    match = re.search(r'^```ts\n(SpotifyPlus\..+?)\n```', original, re.M)
    if not match:
        raise ValueError(f'No signature: {relative}')
    signature = match.group(1)
    heading = signature.split('(', 1)[0]
    heading = heading.split('<', 1)[0].removeprefix('SpotifyPlus.')
    heading += '()'
    summary = original.split(f'# {signature.split("(", 1)[0]}()', 1)[-1].split('## Syntax', 1)[0].strip()
    if not summary or summary.startswith('---'):
        summary = re.search(r'^# .+?\n\n(.+?)\n\n## Syntax', original, re.S | re.M).group(1)
    params_raw = signature.split('(', 1)[1].rsplit('): ', 1)[0]
    return_type = signature.rsplit('): ', 1)[1]
    params = split_parameters(params_raw)
    param_content = ''
    if not params:
        param_content = 'None.\n'
    for param in params:
        name, type_name = param.split(': ', 1)
        optional = name.endswith('?')
        name = name.lstrip('.').rstrip('?')
        explanation = PARAM_OVERRIDES.get(relative, {}).get(name, PARAMS.get(name, 'The value to use for this operation.'))
        param_content += f'`{name}`\n\n{type_badge(type_name)} <Badge variant="{ "neutral" if optional else "danger" }">{ "Optional" if optional else "Required" }</Badge>\n\n{explanation}\n\n'
    returns = re.search(r'^## Returns\n\n(.+?)(?=\n## |\Z)', original, re.S | re.M).group(1).strip()
    remarks_match = re.search(r'^## Remarks\n\n(.+?)\s*\Z', original, re.S | re.M)
    remarks = remarks_match.group(1).strip() if remarks_match else ''
    code = EXAMPLES[relative]
    language = 'tsx' if '<' in code and '/>' in code else 'ts'
    description = 'The following example shows a typical use of this method in an extension.'
    page = f"---\nsidebar_label: '{heading.split('.')[-1]}'\n---\n\nimport CodeBlock from '@theme/CodeBlock';\nimport Badge from '@site/src/components/Badge';\n\n# {heading}\n\n{summary}\n\n## Syntax\n\n{linked_syntax(signature)}\n\n## Examples\n\n{description}\n\n```{language}\n{code}\n```\n\n## Parameters\n\n{param_content}## Returns\n\n`{return_type}`\n\n{returns}\n"
    if remarks:
        page += f'\n## Remarks\n\n{remarks}\n'
    destination = path.with_suffix('.mdx')
    destination.write_text(page, encoding='utf-8')
    if destination != path:
        path.unlink()

paths = sorted(path for path in ROOT.rglob('*.md') if path.relative_to(ROOT).with_suffix('').as_posix() in EXAMPLES)
assert len(paths) == len(EXAMPLES), (len(paths), len(EXAMPLES), set(EXAMPLES) - {path.relative_to(ROOT).with_suffix('').as_posix() for path in paths})
for path in paths:
    rewrite(path)
print(f'Reworked {len(paths)} method pages')
