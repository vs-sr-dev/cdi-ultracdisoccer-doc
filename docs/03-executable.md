# 03 — The executable

`/CMDS/cdi_demo`, 229,376 bytes, dated 1997-05-22 14:53:30 — the last file
written before mastering. It is the whole game: menus, match engine, team
database, fonts, error screens.

CD-i players run **CD-RTOS**, Philips' build of Microware OS-9/68000 on a
68000-family CPU. Executables are relocatable modules, each opening with the
`$4AFC` sync word and closing with a 24-bit CRC. `tools/os9mod.py` parses them
and checks both the header parity word and the CRC.

## Two modules in one file

```
python tools/os9mod.py

module @ 0x000000  'cdi_main.mod'
  size        229,006 bytes   sysrev 1  edition 0
  type/lang   Prgrm / 68000 object
  attr/rev    0x80 (reentrant) rev 0   access 0x0555   owner 1.0
  parity      0x0773 OK   crc24 0x632925 OK
  M$Exec      0x0077a4    M$Excpt 0x000000
  M$Mem       29,212 B static   M$Stack 5,000 B
  M$IData     0x0348b8    M$IRefs 0x0378b2
  M$Init      0x000000    M$Term  0x000000

module @ 0x037e8e  'cdi_syst'
  size        370 bytes   sysrev 1  edition 0
  type/lang   Trap / 68000 object
  attr/rev    0xa0 (reentrant,sticky) rev 0   access 0x0555   owner 0.0
  parity      0x1b1c OK   crc24 0xde6f8a OK
  M$Exec      0x000082    M$Excpt 0x000000
  M$Mem       28 B static   M$Stack 0 B
  M$IData     0x000142    M$IRefs 0x000166
  M$Init      0x000050    M$Term  0x0000d8

trailing 370 bytes after last module (0x37e8e..0x38000)
```

Both CRCs verify against the shipped bytes, so nothing here has been patched
after the link.

**Module 1 is the game.** It asks the system for 29,212 bytes of static
storage and a 5,000-byte stack, and it is re-entrant, which on OS-9 means the
code segment can be shared. Entry is at `+0x77A4`; there is no init or
termination routine and no exception entry, so the module does its own
cleanup.

**Module 2, `cdi_syst`, is a trap handler** — OS-9 module type `$B`, the
mechanism OS-9/68000 uses for shared library calls dispatched through the
68000 `TRAP` instruction. It is 370 bytes, sticky (stays loaded once its use
count drops to zero), owned by the super-user, and it *does* have both an init
(`+0x50`) and a termination routine (`+0xD8`). Module 1 names it in a string
at `0x2D9A8`, right next to `line_event` — an OS-9 event name — so the pair is
almost certainly the game's line-interrupt hook: `cdi_syst` installs the
handler and signals the event, and the game waits on it.

The file is 229,376 bytes; the two modules end at 229,376 exactly. There is no
slack.

## The name it never lost

The disc entry is `cdi_demo`. The module inside is `cdi_main.mod`. The volume
descriptor's application field is `CMDS/cdi_demo`. Whatever this started life
as, it kept the filename all the way to the glass master; see
[11-leftovers.md](11-leftovers.md).

## An 8×8 font in the module header

The module body starts at `+0x50`, immediately after the program header, and
the first thing in it is not code:

```
0x0050  7c c6 c6 fe c6 c6 c6 00     A
0x0058  fc c6 c6 fc c6 c6 fc 00     B
0x0060  7c c6 c0 c0 c0 c6 7c 00     C
0x0068  fc c6 c6 c6 c6 c6 fc 00     D
0x0070  fe c0 c0 f8 c0 c0 fe 00     E
0x0078  fe c0 c0 f8 c0 c0 c0 00     F
```

A one-bit-per-pixel 8×8 alphabet, linked in ahead of everything else. It runs
`A` to `Z` and then stops after three punctuation marks — full stop, comma,
slash — 29 glyphs, 232 bytes, `0x0050` to `0x0137`. Not a digit in it.

This is the font the loader error screens are drawn with — they have to be drawable
before any file has been read, so the glyphs cannot live in `PERM_GFX` like the
rest of the fonts do ([06-fonts.md](06-fonts.md)). Because the only text they
ever draw is those seven fixed messages, the alphabet was cut down to exactly
the characters those messages need.

## The failure paths come first

The lowest string addresses in the module are all things going wrong:

```
0x02BE8   YOUR DISK MAY BE DIRTY OR DAMAGED. ... CONSULT YOUR CDI SUPPLIER.
0x02D08     A PROBLEM OCCURRED WHILE LOADING..
0x02D32          .. COULD NOT OPEN FILE
0x02D5B        .. FAILED DURING FILE READ
0x02D84          .. MEMORY ALLOC ERROR
0x02DAD        .. COULD NOT CLOSE A FILE
0x02DD6        .. COULD NOT GET FILE SIZE
0x02F12   Error Freeing Memory!
```

Five named failure modes for a five-call file API — open, read, size, close,
free — each with its own centred line, and a full-screen apology above them.
The second copy of the "dirty disk" text at `0x02DFF` is the same message
re-broken into 37-column lines, which is the width an 8×8 font reaches across
a 384-pixel screen with a small margin.

Immediately after them, at `0x02F2C`, the path table begins: 128 literal disc
paths, in load order, starting with the five pitches.

## Layout of the module

| Range | Contents |
|---|---|
| `0x00000` – `0x0004F` | module header (48 bytes) + program header (32) |
| `0x00050` – `0x00137` | the 29-glyph 8×8 loader font |
| `0x00138` – `0x02BE7` | code |
| `0x02BE8` – `0x02F2B` | loader and error text |
| `0x02F2C` – `0x03976` | 128 disc path strings |
| `0x03978` – `0x19B45` | code, with the rights notice at `0x05690`, the cartridge warning at `0x05B0E` and the credit roll at `0x06E57` |
| `0x19B46` – `0x1A2A0` | menu text, sound test table, commentary, the placeholder copyright |
| `0x1A2A0` – `0x1ABAB` | fixed tables, and two 588-byte records seeded with `ROTHERHAM UNITED` and `MANCHESTER UNITED` |
| `0x1ABAC` – `0x2D8D7` | the team database — 75 records of 1,028 bytes ([09](09-team-database.md)) |
| `0x2D8D8` – `0x3489F` | code |
| `0x348AA` – `0x348B7` | module name `cdi_main.mod` |
| `0x348B8` – `0x378B1` | initialised data (`M$IData`) |
| `0x378B2` – `0x37E8D` | data reference lists (`M$IRefs`), 1,500 bytes of relocations |
| `0x37E8E` – `0x37FFF` | the `cdi_syst` trap module |

## Reproducing

```
python tools/os9mod.py [FILE]        module headers, parity, CRC
python tools/cdistrings.py [FILE]    paths and text, accidental ASCII filtered out
```
