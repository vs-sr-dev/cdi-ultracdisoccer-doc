# 00 — Overview

## The release

*Ultra CD-i Soccer* is a Philips CD-i football game, developed by **Krisalis
Software Ltd** and published by **Philips Interactive Media** in 1997, the
format's last full year. It is one of a handful of CD-i titles that will not
start at all without the Digital Video cartridge fitted — it ships a
full-screen refusal instead ([08-digital-video.md](08-digital-video.md)).

The studio's home town is written all over the disc: record 72 of the team
database is **Rotherham United**, the only squad in the game whose players are
spelled correctly, and record 73 is the staff
([11-leftovers.md](11-leftovers.md)).

Nothing on the disc calls it *Ultra*. The volume identifier is `CD-i Soccer`,
the title logo reads **CD-i SOCCER**, and the two text files pressed onto the
disc — `abstract` and `biblio` — both open with the line `CD-i Soccer`. The
"Ultra" is packaging.

## The disc

| | |
|---|---|
| Image | `Ultra CD-i Soccer (Europe).chd`, 7,946,573 bytes |
| Track | one, `MODE2_RAW`, 7,875 sectors = 18,522,000 bytes = 1 min 45 s |
| Volume identifier | `CD-i Soccer` |
| System identifier | `CD-RTOS` |
| Publisher | `Philips Interactive Media` |
| Application | `CMDS/cdi_demo` |
| Volume created | 1997-05-22 14:56:09 |
| Volume space | 7,575 blocks of 2,048 bytes |
| Contents | 12 directories, 144 files, 10,635,729 bytes |

A CD holds 333,000 sectors. This disc uses 7,875 of them — **2.4 % of a CD**.
The whole game, video included, would fit twice over on a floppy-sized fraction
of the medium it shipped on.

Work with it like this:

```
chdman extractcd -i "Ultra CD-i Soccer (Europe).chd" \
                 -o _work/ultrasoccer.cue -ob _work/ultrasoccer.bin
python tools/cdifs.py extract _work/files
```

Everything in `tools/` then reads `_work/ultrasoccer.bin` by default.

## What is on it

| Path | Files | Bytes | Contents |
|---|---:|---:|---|
| `/` | 36 | 1,648,293 | boot text, the "no cartridge" screen, the tactics grid, and an entire abandoned localisation set |
| `/CMDS` | 1 | 229,376 | `cdi_demo` — the game, two OS-9/68000 modules |
| `/RTF` | 1 | 4,079,616 | `intro_anim` — the MPEG-1 intro |
| `/SAMPLES` | 12 | 128,778 | sound effects, AIFF-C with CD-i ADPCM |
| `/PERM_GFX` | 10 | 97,856 | fonts, pointer, loading picture — the always-resident set |
| `/INTRO_GFX` | 11 | 481,696 | Philips and Krisalis logos, title, credits backdrop |
| `/TSELECT_GFX` | 4 | 139,682 | team select |
| `/TOURN_GFX` | 19 | 573,056 | tournament screens, option backdrops, kit swatches |
| `/PLAYER_SPRTS` | 11 | 624,640 | ten outfield kits and the goalkeeper |
| `/PITCH_GFX` | 25 | 2,002,848 | five pitches, goals, ball, referee, tactics font |
| `/SCOREBOARD_GFX` | 2 | 92,544 | the stadium scoreboard |
| `/SAD_GFX` | 5 | 207,424 | the dejection screen |
| `/CELEB_GFX` | 7 | 329,920 | the celebration screen and three trophies |

The full listing with sector addresses, sizes, dates and attributes is in
[notes/file-inventory.md](../notes/file-inventory.md).

## Provenance from the timestamps

Every directory entry carries a six-byte date. Grouped by month:

```
1996-04  42 files      1996-09  31 files      1997-01  13 files
1996-05   4            1996-10   6            1997-02   6
1996-06   2            1996-11   2            1997-04   2
1996-07  17            1996-12   2            1997-05   3
1996-08  14
```

The oldest file is `/ip_gfx` at **1996-04-09 12:23:24**; the newest is the
real-time file at **1997-05-22 14:55:34**, thirty-four seconds before the
volume descriptor was written. Two clusters stand out: a burst of 42 files in
April 1996 that is almost entirely the abandoned localisation set, and the 1997
files, which are the intro sequence, the credits, the tactics screen and the
executable — the last things finished.

The twelve directories all carry 1997-05-22 14:55:33–14:56:07: they were
created by the mastering pass, not by the artists.

## Reading order

| Doc | Contents |
|---|---|
| [01-disc-image.md](01-disc-image.md) | The track, the sector map, and 5 MB of scrambled audio in front of the file system |
| [02-filesystem.md](02-filesystem.md) | Green Book volume descriptor, path table, directory records, the case clash |
| [03-executable.md](03-executable.md) | `cdi_demo`: two OS-9/68000 modules, memory, entry points, the font in the header |
| [04-graphics.md](04-graphics.md) | Raw CLUT bitmaps, palette files, resolutions, the 512-byte line pitch |
| [05-sprites.md](05-sprites.md) | `rlspr`: fixed slots, run-length lines, 416 frames per kit |
| [06-fonts.md](06-fonts.md) | Four fonts in three different layouts, one of them code page 437 |
| [07-audio.md](07-audio.md) | AIFF-C with an `APCM` chunk, Level C ADPCM, and a Sound Designer II fingerprint |
| [08-digital-video.md](08-digital-video.md) | The real-time file, MPEG-1 at 368×272, and why the cartridge is mandatory |
| [09-team-database.md](09-team-database.md) | 75 teams, 1,454 players, and the fields that are still unread |
| [10-text-and-ui.md](10-text-and-ui.md) | Menus, commentary, the sound test, the error screens |
| [11-leftovers.md](11-leftovers.md) | The archaeology: dead files, dead languages, a Sega logo, and a swear word |
| [12-open-questions.md](12-open-questions.md) | What is still unresolved, with the measurements behind it |
