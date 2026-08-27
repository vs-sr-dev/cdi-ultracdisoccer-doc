# 04 — Graphics

Nothing in this game is compressed. Every `_gfx` file, every background, every
pitch is a flat array of one-byte CLUT indices with no header, no dimensions,
no magic number and no run-length coding — the file *is* the framebuffer. The
only exception is the sprite banks, which use a small run-length scheme of
their own ([05-sprites.md](05-sprites.md)).

That is a reasonable choice on CD-i. The MCD212 video chip reads CLUT7 and
CLUT8 planes straight out of memory, so a picture loaded from disc is a picture
in the display list one `memcpy` later. The cost is disc space, and the disc is
2.4 % full.

## Palettes

A `_pal` file is a flat list of RGB triplets, one byte per component, high
nibble significant. There are exactly three sizes, and they are the three CD-i
CLUT bank counts:

| Size | Entries | Banks | Used by |
|---:|---:|---:|---|
| 192 | 64 | 1 | pitch overlay, tactics, options, celebration |
| 384 | 128 | 2 | most full-screen art |
| 768 | 256 | 4 | the intro logos, `nodv`, `opt_baks`, `ballback` |

Entry 0 is the transparency key. In almost every palette on the disc it is
`#00FF00`, pure green; `mypointa_pal` uses white instead.

Pixel values back this up. The full-screen backgrounds top out at 126 or 127
and never reach 128 — they are **CLUT7**, the 128-colour mode CD-i uses for a
normal-resolution plane. The 64-entry palettes belong to files whose pixel
values stop at 63 (`celeb_gfx`, `sadomar1/2_gfx`) or 31.

## Resolutions

The CD-i normal-resolution frame is 384 pixels wide. Everything full-screen on
this disc is 384 across:

| Size | Geometry | Files |
|---:|---|---|
| 92,160 | 384 × 240 | `logo_gfx`, `krislogo`, `philbump`, `credback`, `eng_introb_gfx`, `andrea_gfx`, `scorbord_gfx`, `sadback_gfx`, `ballback`, `eng_tselect_gfx` |
| 107,520 | 384 × 280 | `credback280` |
| 368,640 | 384 × 240 × 4 | `opt_baks` — four option backdrops in one file |
| 48,000 | 320 × 150 | `eng_knockout_gfx` |
| 71,680 | 320 × 224 | the abandoned localisation set ([11](11-leftovers.md)) |
| 57,344 | 256 × 224 | `sadomar1_gfx`, `sadomar2_gfx` |
| 8,192 | 128 × 64 | `loading_pic` |

`credback` and `credback280` are the same credits backdrop at 240 and 280
lines — the NTSC and PAL heights of a CD-i normal-resolution screen. The disc
is the European release and carries both.

## The 512-byte line pitch

Two files are 122,880 bytes, which is not a multiple of 384. They are
**384 pixels of picture in a 512-byte line**: 512 × 240 = 122,880, with the
right 128 columns left as filler.

```
nodv_gfx          512 x 240, picture in columns 0..383
eng_tscreen_gfx   512 x 240, picture in columns 0..383
```

`nodv_gfx` is the "you do not have your Digital Video Cartridge loaded" screen;
`eng_tscreen_gfx` is the Tacti-Grid, the squad and formation screen the
`abstract` file advertises as "the innovative Tacti-Grid (TM)". Rendering
either at 384 shears it into diagonal noise, which is exactly what happens if
you assume a pitch equal to the width.

The five pitches use the whole 512:

```
nmlpitch drypitch mudpitch icepitch wetpitch    512 x 768, 393,216 bytes each
```

512 × 768 is the entire playing surface, goal to goal, in one bitmap: the
screen shows 384 × 240 of it and scrolls. Five weather variants — normal, dry,
muddy, icy, wet — 1.9 MB of grass, which is 18 % of everything on the disc.
The menu only offers three (`Normal`, `Muddy`, `Frosty`).

512 is a power of two, and a power-of-two line pitch turns the multiply in a
scrolling blitter's address calculation into a shift. That is why the two
screens that scroll and the two screens that do not all agree on it.

## Palette pairing

There is no index inside a `_gfx` file saying which palette to use; the
pairing lives in the executable, which loads them together. `tools/cdigfx.py`
carries the same table, worked out from the load order of the 128 path strings
at `0x02F2C` and confirmed by eye.

Six palettes have no obvious partner because the graphic they belong to is not
on the disc at all: `tmsplng_pal` (for the missing `/tmsplng_gfx` and
`/tmsplng2_gfx`), and the three `<lang>_intro_pal` files whose pictures are
blank. See [11-leftovers.md](11-leftovers.md).

## A palette that is not finished

`CELEB_GFX/celeb_pal` is 192 bytes — 64 entries — of which entry 0 is the
green key and the remaining 63 hold only 15 distinct colours, arranged as a
16-entry block repeated four times. `celeb_gfx` itself is 245,760 bytes of
pixels in the range 0–31. Rendered against its own palette, the celebration
artwork comes out in two colours.

Either the game supplies a different CLUT at run time, or this palette shipped
half-written. It is [an open question](12-open-questions.md).

## Reproducing

```
python tools/cdigfx.py sheet OUTDIR              render everything with a known layout
python tools/cdigfx.py render FILE -p PAL -w W   one file, your own guess
python tools/cdigfx.py pal FILE                  print a palette as hex
```
