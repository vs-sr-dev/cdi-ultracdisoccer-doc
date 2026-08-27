# cdi-ultracdisoccer-doc

Reverse-engineering notes on **Ultra CD-i Soccer** (Krisalis Software /
Philips Interactive Media, 1997) — a football game released in the Philips
CD-i's final year, and one of the few titles on that format that refuses to
start at all without the Digital Video cartridge fitted.

This repository documents the European release: a single-track disc holding
144 files, one OS-9/68000 executable, and a 4 MB MPEG-1 intro. Nothing on the
disc is compressed. Almost nothing on the disc is called what you expect.

**Documentation only.** No game assets, no extracted art, no audio, no
executable code is committed here. The tools in [`tools/`](tools/) reproduce
every figure, table and image in these pages from your own legally obtained
copy.

## What is documented

| Doc | Contents |
|---|---|
| [00-overview.md](docs/00-overview.md) | The release, the disc, the file inventory, what the timestamps say about the schedule |
| [01-disc-image.md](docs/01-disc-image.md) | The track, the sector map, and 5.2 MB of scrambled audio in front of the file system |
| [02-filesystem.md](docs/02-filesystem.md) | Green Book volume descriptor, path table, directory records, attributes, a case clash |
| [03-executable.md](docs/03-executable.md) | `cdi_demo`: two OS-9/68000 modules, memory, entry points, and a 29-glyph font in the header |
| [04-graphics.md](docs/04-graphics.md) | Raw CLUT bitmaps, palette files, resolutions, and the 512-byte line pitch |
| [05-sprites.md](docs/05-sprites.md) | `rlspr`: fixed 128-byte slots, run-length lines, 416 frames per kit |
| [06-fonts.md](docs/06-fonts.md) | Four fonts in three layouts, one of them an IBM PC code page |
| [07-audio.md](docs/07-audio.md) | AIFF-C with an `APCM` chunk, Level C ADPCM, and a Sound Designer II fingerprint |
| [08-digital-video.md](docs/08-digital-video.md) | The real-time file, MPEG-1 at 368×272, and the screen that says no |
| [09-team-database.md](docs/09-team-database.md) | 75 teams, 1,454 players, and the fields still unread |
| [10-text-and-ui.md](docs/10-text-and-ui.md) | Menus, commentary, the credit roll, two copyright notices |
| [11-leftovers.md](docs/11-leftovers.md) | The archaeology: dead files, dead languages, a Sega logo, a swear word |
| [12-open-questions.md](docs/12-open-questions.md) | Everything unresolved, with the measurements behind it |
| [notes/file-inventory.md](notes/file-inventory.md) | All 156 directory entries with LBA, size, date and attributes |
| [notes/graphics-inventory.md](notes/graphics-inventory.md) | Every bitmap and palette, with geometry and pixel range |
| [notes/team-database.md](notes/team-database.md) | All 75 squads, every player, flags and ratings |
| [notes/string-inventory.md](notes/string-inventory.md) | Every legible string in the executable, grouped |
| [notes/cdi-platform-notes.md](notes/cdi-platform-notes.md) | **Platform checklist** — what to look for on *any* CD-i disc, written for the next title |

## Highlights

**Nothing on this disc is compressed, and 2.4 % of the disc is used.** A CD
holds 333,000 sectors; this game occupies 7,875. Every background is a flat
array of one-byte CLUT indices with no header and no encoding — the file *is*
the framebuffer, and a picture loaded from disc is a picture on screen one
`memcpy` later. The only coded format is the player sprites, and it exists
because a running footballer is mostly transparent.

**5.2 MB in front of the file system is scrambled audio the game cannot
reach.** Sectors 0–2268 are well-formed Mode 2 Form 2 sectors — correct sync,
correct header, correct EDC — whose user data is the **ECMA-130 scrambler
sequence**. XOR it back out and 1,064 sectors are zeroes and 1,203 become
15.7 seconds of 16-bit PCM at 44.1 kHz, mono content in a stereo container,
left channel identical to right in all 692,928 frames. Two clips, 7.41 s and
8.31 s, harmonic, uncorrelated with each other. The zero padding at the *other*
end of the disc is plain zeroes, so two different filler mechanisms are at work
in one image. What the audio is remains
[open](docs/12-open-questions.md).

**The disc has never heard of "Ultra".** The volume identifier is `CD-i
Soccer`. So is the volume set identifier, and the first line of both text files
pressed onto the disc, and the title bitmap. The boot application is
`CMDS/cdi_demo`; the OS-9 module inside it is `cdi_main.mod`. Four names, none
of them the one on the box.

**Ten per cent of the file system is empty files.** Sixteen files totalling
1,070,080 bytes contain nothing but zero bytes: German, French and Spanish
versions of five screens each, stamped April 1996 and pressed onto the glass
master thirteen months later at full size. Their *palettes* are real — three
192-byte CLUTs with genuine, distinct colours — so somebody chose the colours
for each language before the pictures were abandoned.

**The executable asks for a Sega logo.** `/segalogo_gfx` and `/segalogo_pal`
sit in the middle of the load table, between the scoreboard palette and the
tactics palette, and neither file is on the disc. The abandoned root-level art
is 320 × 224 — a Mega Drive PAL frame, not a CD-i one — and the credits thank
**Cross Products**, who made the SNASM 68000 development systems that British
studios used for Sega work.

**Two of those 320 × 224 files are the Manchester United club crest**, and a
third is a photograph of a United player lifting the Premier League trophy in a
Sharp-sponsored shirt. The executable loads two of the three — `eng_introf_gfx`
is the crest, `eng_introb_gfx` the photograph, front layer over back — while
renaming `Ian Wright` to `Ian Write`, `David Seaman` to `David Sceaman` and
`Graeme Le Saux` to `Graeme Le-Sawx`, as every unlicensed football game of the
period did.

**The developers put themselves in the game, twice.** Record 72 of the team
database is **Rotherham United** — the studio's local club, third tier, and the
only squad in the game whose twenty-one names are spelled correctly. Record 73
is **Krisalis**, eighteen staff as a playable team, rated from 89 down to a
player called `DeeDee` with zero in seven of nine attributes. Record 74 is
`Ken Dodds dads dogs dead` of `FUG land`, short name `Too Good`, twenty-one
players at 100 in everything, mixing Baggio, Romario and Bergkamp under their
real names with `Eric Cantonarse`.

**A placeholder copyright shipped.** Between `League Drawn` and the sound-test
table, laid out as three screen lines:

```
La di da ... Put some copyright
Message crap in here or something
Written by Krisalis etc etc etc
```

The real notice is elsewhere in the binary and is the one that gets drawn.

**The string system has an error message and it is not polite.** At `0x1A1C3`,
five bytes after the last commentary line: `Fuckin' strings fucked`. Also on
the disc: `CHEAT MODE ON`, `QUIT`, `GAME WINDOW`, `TV`, `MONITOR`.

**The sound effects are Macintosh files.** Twelve AIFF-C containers whose
sample data lives in a non-standard `APCM` chunk: Green Book ADPCM, four bits
at 18,900 Hz, CD-i Level C. Three of them — the goal cheer and two near-misses,
recorded three weeks after the rest — still carry a 424-byte `Sd2a` chunk from
**Digidesign Sound Designer II**. Total playing time of every sound in the
game: 10.2 seconds.

**Eight pieces of music are named and none of them ship.** `TITLE THEME`,
`CREDITS`, `WIN EUROPEAN CUP` and five more are entries in a sound test that
also has a `TEST TUNE` menu item and a `MUSIC` toggle. The other thirteen
entries map onto the twelve files in `/SAMPLES` exactly. No file on this disc
holds a tune.

**The font is a DOS code page.** 139 glyphs in `msfont_sprts`, and the block
above ASCII reads `Ç ü é â ä à å ç ê ë è ï î ì Ä Å É æ Æ ô ö ò û ù ÿ Ö Ü ¢ £ ¥
₧ ƒ á í ó ú ñ Ñ ª º ¿` — IBM CP437, `0x80` to `0xA8`, in order, peseta sign and
all. On a 68000 running OS-9. The game never prints an accented character.

**The pitch is 512 × 768 and there are five of them.** 1.9 MB of grass, 18 % of
everything in the file system, for three weather settings on the menu. The
line pitch is 512 because a power of two turns a scrolling blitter's multiply
into a shift — and the two full-screen images that do *not* scroll, `nodv_gfx`
and the Tacti-Grid, use the same 512-byte stride with 384 pixels of picture and
128 columns of nothing.

## Tools

Pure Python 3. `pillow` is needed for the rendering paths; nothing else.

```
tools/cdilib.py      sectors, subheaders, the Green Book file system
tools/cdifs.py       list / tree / extract / sector map
tools/cdihead.py     the pre-file-system region: descramble, classify, dump the audio
tools/os9mod.py      OS-9/68000 module headers, parity and CRC-24
tools/cdistrings.py  strings, with 68000 object-code noise filtered out
tools/cdigfx.py      CLUT bitmaps and palettes -> PNG
tools/cdispr.py      the rlspr sprite banks -> contact sheets
tools/cdiaudio.py    AIFF-C / APCM parsing and a CD-i Level B/C ADPCM decoder
tools/cdirtf.py      the real-time file: census, demux, MPEG headers
tools/cditeams.py    the team and player database
```

Start here:

```
chdman extractcd -i "Ultra CD-i Soccer (Europe).chd" \
                 -o _work/ultrasoccer.cue -ob _work/ultrasoccer.bin
python tools/cdifs.py extract _work/files
python tools/cdifs.py map
python tools/cdihead.py map
python tools/os9mod.py
python tools/cditeams.py list
```

Everything defaults to `_work/ultrasoccer.bin` and `_work/files/`, and `_work/`
is git-ignored.

## Working on another CD-i disc?

[notes/cdi-platform-notes.md](notes/cdi-platform-notes.md) is a checklist
distilled out of this one: sector and Green Book layouts, the scrambler test for
the pre-file-system region, OS-9 module validation, how to find a bitmap's width
(and why 512 will catch you out), the ADPCM sound-group layout, real-time file
demuxing, and the order of work that turned out to pay best. Six of the ten
tools here are platform-general and should run unmodified.

It also records this disc's numbers as a baseline, so you can tell what is
normal for CD-i from what your title is doing differently.

## Scope

This is a **documentation** pipeline. There is no port, no patch, no
reimplementation here, and no plan for one in this repository. What is here is
a description of how the disc is put together, accurate to the byte where it
claims to be, and honest about the parts that are still guesses — those are
collected in [12-open-questions.md](docs/12-open-questions.md).

Corrections and answers to the open questions are welcome.
