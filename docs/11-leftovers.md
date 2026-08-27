# 11 — Leftovers

## The disc is not called what the box is called

Nothing inside this disc says *Ultra*.

```
volume identifier         CD-i Soccer
volume set identifier     CD-i Soccer
abstract file, line 1     CD-i Soccer
biblio file, line 1       CD-i Soccer
INTRO_GFX/logo_gfx        the title art, reading "CD-i SOCCER"
```

The title bitmap is a green-keyed 384 × 240 screen with `CD-i` in blue above a
chrome `SOCCER`, and underneath, in small type:

```
(c) 1997 Philips Interactive Media
Design and Code by Krisalis Software
```

The "Ultra" was added at packaging, after 1997-05-22 14:56:09, when the volume
descriptor was written.

## The boot application is called `cdi_demo`

```
volume descriptor, application identifier    CMDS/cdi_demo
directory entry                              /CMDS/cdi_demo
OS-9 module 1 name                           cdi_main.mod
OS-9 module 2 name                           cdi_syst
```

The path a CD-i player follows to start this game leads to a file called
`cdi_demo`, and the module inside it is called `cdi_main.mod`. Three names for
one program, none of them the game's.

## A million bytes of nothing, in three languages

Sixteen files on this disc contain no data at all — every byte is zero:

```
ger_introb_gfx   71,680     fra_introb_gfx   71,680     spa_introb_gfx   71,680
ger_introf_gfx   71,680     fra_introf_gfx   71,680     spa_introf_gfx   71,680
ger_tscreen_gfx  71,680     fra_tscreen_gfx  71,680     spa_tscreen_gfx  71,680
ger_tselect_gfx  71,680     fra_tselect_gfx  71,680     spa_tselect_gfx  71,680
ger_knockout_gfx 46,080     fra_knockout_gfx 46,080     spa_knockout_gfx 46,080
ip_gfx           71,680
```

**1,070,080 bytes — 10 % of the file system — is empty files.**

German, French and Spanish versions of five screens each: the two intro
layers, the Tacti-Grid, team select and the knockout bracket. All three
languages, all five screens, all zero. They are stamped 1996-04-11, and they
were pressed onto the glass master thirteen months later at full size.

The palettes survived. `ger_intro_pal`, `fra_intro_pal` and `spa_intro_pal` are
192 bytes each of real colour data — dark, muted, different from one another —
so somebody got as far as choosing a CLUT for each language before the pictures
were abandoned. That is the order these things happen in: the palette comes out
of the art tool with the first draft.

The executable never names any of them. It names the English ones —
`/eng_introb_gfx`, `/eng_introf_gfx`, `/eng_tscreen_gfx` — and those are the
copies that work.

## The Sega logo

At `0x03199` and `0x031A7` in `cdi_demo`:

```
/segalogo_gfx
/segalogo_pal
```

Neither file is on the disc. They sit in the middle of the load table between
`/SCOREBOARD_GFX/scorbord_pal` and `/PITCH_GFX/tacti_pal`, in the same list as
every other picture the game opens.

They are not alone. The abandoned root-level art is **320 × 224** — not the
384 × 240 or 384 × 280 of a CD-i normal-resolution plane, but the frame a Sega
Mega Drive puts on a PAL television. The credits thank **Cross Products**,
whose SNASM systems were the standard 68000 development kit for Mega Drive and
Saturn work in Britain.

`eng_introf_gfx` and `intro_gfx`, both 320 × 224, both from that set, are the
**Manchester United club crest** — the real thing, "MANCHESTER UNITED FOOTBALL
CLUB" around the ship and the devil, in two palettes. The only team blurb ever
written is Manchester United's. `eng_introb_gfx`, 384 × 240 and re-drawn at
CD-i size, is a photograph of a Manchester United player in a Sharp-sponsored
shirt holding the Premier League trophy over his head.

The executable loads two of the three: `/eng_introb_gfx` and `/eng_introf_gfx`
are both in the load table, back layer and front layer of the same screen.
`intro_gfx`, the second copy of the crest, is named by nothing.

A game that changes `Ian Wright` to `Ian Write` ships the club crest at full
size and a licensed press photograph, and puts both on screen.

## Files the game asks for that are not there

Eleven path strings in `cdi_demo` do not resolve to a directory entry. Two are
the NVRAM device and one is a false positive out of the team table; the other
eight are real:

| Path | What it was |
|---|---|
| `/segalogo_gfx`, `/segalogo_pal` | see above |
| `/comment_gfx` | the backdrop the commentary lines were to be drawn on |
| `/ocean6a_gfx`, `/ocean6a_pal` | unidentified — a background named for something |
| `/tmsplng_gfx`, `/tmsplng2_gfx` | the palette `/TOURN_GFX/tmsplng_pal` is on the disc; its two pictures are not |
| `/kit1_rlspr` | the sprite format carrying its own name, on a file superseded by `PLAYER_SPRTS/kit1_sprts` |

And 23 files on the disc are never named by the executable: the sixteen blank
localisation files, their five palettes, `intro_gfx`, and `PATH_TBL`.

## Two teams that are not football teams, and one that is a joke

Records 72, 73 and 74 of the team database:

**72 — Rotherham United.** The Krisalis local club, third tier, with all
twenty-one names spelled correctly while every top-flight squad on the disc is
deliberately misspelled. Lee Glover, Shaun Goater, Ian Breckin, Chris Wilder,
Paul Hurst, Steve Cherry, John McGlashan, Trevor Berry, Andy Roscoe — the
mid-1990s squad, right.

**73 — Krisalis.** The studio, as a playable team, eighteen players, ratings
descending from good to comic:

```
Ramo               80 59 57 78 68 63 36 59 61
Mark Adamson       76 71 46 50 63 85 26 49 48
Neil Adamson       89 93 47 54 56 48 64 53 78
Phil Hackney       72 52 43 50 41 50 48 68 53
Steve Colledge     79 47 73 64 70 55 61 66 51
Dave Colledge      59 57 63 67 62 53 50 32 57
Mark Potente       69 67 73 32 25 33 28 36 25
Marvyn Burton      63 59 37 50 74 75 32 51 44
Andy Ware          57 58 48 56 51 44 39 30 42
Mark Edwards       78 64 50 52 62 55 52 43 42
Tim James          72 82 42 39 32 15 40 48 34
Mark Incley        73 36 53 19 10 15 10 15 19
Paul Kirk          68 64 69 32 25 24 34 32 28
Simeon Pashley     67 53 51 36 28 42 45 34 26
Tracy Hudson       20 40 36 34 10  2  5 45 23
Pete Harrap        21 29 14 15 15  3  3  1  4
Siobhan Moron      23 22  8  8  7  7  6  6 10
DeeDee             37  7  0  5  0  0  0  0  0
```

Every name in the credit roll is in that list. **Pete Harrap**, who wrote the
arcade engine and is thanked separately for "Sorting it out!!", is third from
bottom.

**74 — `Ken Dodds dads dogs dead`, of `FUG land`, short name `Too Good`.**
Twenty-one players, every one of them 100 in all nine attributes, mixing real
1990s stars under their real names — Roberto Baggio, Romario, Franco Baresi,
Dennis Bergkamp, Gabriel Batistuta, Gianfranco Zola, Alen Boksic, Faustino
Asprilla, Gianluigi Lentini, Basile Boli — with Krisalis surnames given
continental first names: `Marcus Adamson`, `Stephano Bielby`, `Andreas
Whiteley`, `Benito Walshaw`, `Ricardo Oldale`, `Christo Shoreo`, `Craig
Watkinson`, and `Eric Cantonarse`.

It is the only record in the database whose player flags byte has bit 7 clear
on all twenty-one rows — the rest of the game sets it on 1,433 of 1,454
players. Someone typed this team in through a different door.

## Debug strings

```
0x1A1C3   Fuckin' strings fucked
0x2E64B   QUIT   GAME WINDOW
0x2EA9D   TV   MONITOR
0x30368   Start (.)    Cancel (..)
0x3383C   CHEAT MODE ON
0x33D2C   PRESS : OR ;
```

The first one sits five bytes after the last commentary line
(`That was close!`) and immediately before the Manchester United blurb. It is
an error message for the string system, in a retail Philips product, on a
pressed disc.

`TV` / `MONITOR` and `QUIT` / `GAME WINDOW` are development-host options — a
CD-i emulator card in a development system could put the running game in a
window on a workstation display. `CHEAT MODE ON` is exactly what it says.

## The placeholder copyright

At `0x19F82`, between `League Drawn` and the sound-test table, laid out as
three screen lines:

```
La di da ... Put some copyright
Message crap in here or something
Written by Krisalis etc etc etc
```

The real notice is at `0x05690` and is drawn by a different screen. This one
was written to hold a place, and nobody came back for it.

## `andrea_gfx`

A 384 × 240 image, dated 1997-01-22, paired with its own 256-entry palette: a
close-up of a woman's face, dark, with a floodlit stadium composited across the
eyes and `PHILIPS` legible on the hoardings. The executable loads it
(`/andrea_gfx` at `0x03943`). It is the only asset on the disc named after a
person.

## Small things

- **`PATH_TBL`.** The Green Book path table at LBA 2269 is also a named file in
  the root, 216 bytes, attributes `0x0111`. The authoring tool exposed its own
  index.
- **`intro_gfx` and `INTRO_GFX/`.** A file and a directory with the same name
  modulo case, in the same directory ([02-filesystem.md](02-filesystem.md)).
- **`celeb_pal`.** 64 entries, of which 63 hold fifteen distinct colours in a
  16-entry block repeated four times. The celebration artwork renders in two
  colours against it ([04-graphics.md](04-graphics.md)).
- **The font is a DOS code page.** 139 glyphs of IBM CP437, `0x20` to `0xAA`,
  in a 68000 OS-9 program. Nothing in the game prints an accented character
  ([06-fonts.md](06-fonts.md)).
- **`biblio` says "Pragrammed by".** A typo on a pressed disc, in the file the
  volume descriptor points at as the bibliographic record.
- **Three sounds went through Sound Designer II** and kept the `Sd2a` settings
  chunk; the other nine did not ([07-audio.md](07-audio.md)).
- **Eight pieces of music are named and none of them ship**
  ([07-audio.md](07-audio.md)).
- **Both PAL and NTSC credits backdrops ship.** `credback` is 384 × 240,
  `credback280` is 384 × 280, the same picture, each with its own 256-entry
  palette, both on a European disc.
- **5.2 MB of scrambled audio sits in front of the file system**, the largest
  single thing on this disc that the game does not use
  ([01-disc-image.md](01-disc-image.md)).
