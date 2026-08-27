# 05 — Sprites: the `rlspr` format

Eleven files in `PLAYER_SPRTS` hold the players. They are the only art on the
disc that is not a flat bitmap, and the executable tells you what they are
called: at `0x036B3` there is a path string `/kit1_rlspr` — a **run-length
sprite** — pointing at a file the disc does not carry. The format survived; the
name did not make it onto the disc.

## The format

A bank is a flat array of fixed-size slots. Every player bank uses **128-byte
slots**. Inside a slot the sprite is coded one line at a time:

| Byte | Meaning |
|---|---|
| `0x00`–`0x7F` | one pixel of that CLUT index |
| `0x80`–`0xFD` | skip `n & 0x7F` transparent pixels |
| `0xFF` | end of line |
| `0xFE` | filler — pads the slot out to 128 bytes |

Nothing else. There is no width, no height, no hot spot, no frame count: the
slot index is the frame number, the line count is however many `0xFF` bytes
turn up before the filler starts, and the width is whatever the pixels and
skips add up to.

The first six lines of `kit1_sprts` decode like this:

```
85 03 08 03 ff              skip 5,  pixels 3 8 3
85 08 08 08 ff              skip 5,  pixels 8 8 8
85 03 08 03 ff              skip 5,  pixels 3 8 3
84 02 0e 0e 0e 02 ff        skip 4,  pixels 2 e e e 2
83 02 02 0e 0e 0e 02 02 ff  skip 3,  pixels 2 2 e e e 2 2
84 05 04 81 04 05 ff        skip 4,  pixels 5 4, skip 1, pixels 4 5
```

That last line is the point of the format: a skip code can appear *inside* a
line, so a sprite with a hole in it — the gap between a running player's legs —
costs two bytes.

## What is in the banks

```
python tools/cdispr.py info PLAYER_SPRTS/kit1_sprts
416 slots of 128 bytes
widths  7..16   heights 12..16
empty slots: 0

python tools/cdispr.py info PLAYER_SPRTS/goalie_sprts
720 slots of 128 bytes
widths  0..16   heights 0..16
empty slots: 8
```

| File | Bytes | Slots |
|---|---:|---:|
| `kit1_sprts` … `kit10_sprts` | 53,248 each | 416 |
| `goalie_sprts` | 92,160 | 720 |

**416 frames per outfield kit.** Sixteen pixels wide at the most, sixteen lines
tall at the most — a player on a 384 × 240 screen over a 512 × 768 pitch is a
thumbnail. 416 frames buys running in eight directions, turning, sliding,
jumping, heading, throwing in, being fouled, celebrating; the goalkeeper gets
720 and leaves eight of them empty.

The ten kits are ten separate banks, not one bank with ten palettes: the CLUT
indices differ between files (`kit1_sprts` uses 49 distinct values, `kit2_sprts`
45). Colour is baked in. With 75 teams and 10 kits, teams share.

Total: 624,640 bytes for the players, against 1,966,080 for the five pitches
they run on.

## Rendering them

The banks carry no palette of their own and no `_pal` file sits beside them in
`PLAYER_SPRTS`. `tools/cdispr.py` defaults to `PITCH_GFX/nmlpitch_pal`, which
is the CLUT loaded while a match is on screen; the shapes come out right and
the colours are a guess. Which CLUT the kit indices are meant to land in is
[open](12-open-questions.md).

```
python tools/cdispr.py info FILE
python tools/cdispr.py sheet FILE OUT.png -p PALETTE -c COLUMNS
```

## Other `_sprts` files are not this format

The suffix is not a reliable marker. `msfont_sprts`, `mtfont_sprts`,
`o16x16fnt_sprts`, `t4font_sprts`, `ball_sprts`, `flags_sprts`, `lcd_sprts`,
`shadow_sprts` and `pointer_sprts` all top out well below `0x80` and are plain
bitmaps — see [06-fonts.md](06-fonts.md). Only the eleven player banks are
`rlspr`.
