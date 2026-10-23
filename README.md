# Strain Packs

A collectible strain-card and grow game. Open packs, collect strains, grow and harvest plants in an underground bunker, trim and cure the bud, and sell it in your shop. The whole game is **one HTML file**: open it in any browser (phone or computer) to play.

## Files

| File | What it is |
|---|---|
| `strain-packs.html` | **The main game.** Make changes here. Starts with 400 coins. |
| `strain-packs-test-kit.html` | Testing copy: 250,000 coins plus test tools (for example, force a God Pack). |
| `strain-packs-friends.html` | Friends test copy: starts with 3,000 coins. |

The three files are identical except for one line near the top of the script:

```js
/*BUILD*/const BUILD = {kind:"main", startCoins:400, badge:"", tools:false};/*END BUILD*/
```

The other two versions use `{kind:"test", startCoins:250000, badge:"TEST KIT", tools:true}` and `{kind:"friends", startCoins:3000, badge:"FRIENDS TEST", tools:false}`, and each has its own `<title>`. **Change only `strain-packs.html`**, then copy it over the other two and swap in that line and the title.

## How the file is laid out

- **No `<html>`/`<head>`/`<body>` tags.** The file starts with `<title>` and `<style>`, followed by the page markup, then one big `<script>`.
- All the code is plain JavaScript inside one wrapper, `(() => { "use strict"; ... })()`. There are no libraries and no build step.
- About half the file size is pictures (packs, seed jars, the trim machine, coins and so on) stored inside the file as long `data:image/...;base64,` strings. Don't edit those; you can skip past them.
- Almost everything else (buds, plants, cards, the grower, the shop and customers) is drawn with canvas code.

The script is split into sections, each starting with a comment like `/* ---------- name ---------- */`. Search for these to find your way around:

| Section | What's in it |
|---|---|
| data | Strain list (`STRAINS`), rarities, packs, floors (`FLOORS`) |
| state | The save object `S` and `fresh()` |
| art / full-art backgrounds | Bud drawing, card art, a unique scene for each Mythical card |
| elevator / views | Floor navigation and `render()` |
| booster boxes, ripping a pack | Pack shop, opening packs, God Packs |
| trimming table, the trim machine | Benny the human trimmer and the conveyor trim machine |
| customer orders | Special orders |
| the till / what walk-in customers ask for | Counting change; gram, ounce and pound orders (`SIZES`, `makeOrder`, `fillOrder`) |
| staff (trimmer, grower, cashier) | Hired staff: Benny, the grower (Mari/Marco), Rico the cashier |
| the grower on screen / your grower's look | `drawMari()` draws every person in the game; grower clothes (`GLOOK`) |
| the shop floor / storefront | Animated shop: counter, scale, customers walking in (`paintShop`) |
| breeding rooms, sprays, pests, simulation | Growing logic |
| Grow Pass, Store, plant food, decorations, room looks | Shops and extras |
| friends / online now | Leaderboard, seed trading, grow-off, friends list |
| levels, actions | XP and the main click handler (buttons use `data-*` attributes) |
| plant drawing | Plants in the grow tents |
| saving, account, boot | Save and load, sign-in, start-up |

The screen is redrawn with `render()`. Animations run in `loop()` (requestAnimationFrame), and game logic ticks every 250 ms.

## Features that only work inside Claude

The game was built as a Claude artifact. These parts use Claude's built-in services (`window.claude`) and **do nothing when the file is opened anywhere else**:

- Signing in and saving to your account
- Who's online, friends, seed trading, the leaderboard and the grow-off

Opened anywhere else, the game still plays fully and saves on that device only (browser `localStorage`, key `strain-packs-save`).

## Tips for making changes

- Change one thing at a time, then open the file in a browser and check that it still loads.
- Before adding a CSS class, search the file to make sure the name isn't already used.
- Check it on a phone-sized screen too. The game is built to work on iPhone and Android.
