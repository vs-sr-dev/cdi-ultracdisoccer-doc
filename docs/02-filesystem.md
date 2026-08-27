# 02 — The file system

CD-i uses the Green Book file system: ISO 9660's skeleton with big-endian-only
numbers, a mandatory path table, and a ten-byte system-use area on every
directory record carrying owner and permissions. `tools/cdilib.py` implements
it in about eighty lines.

## Volume descriptor, sector 16

```
offset  field                     value
0       descriptor type           1
1       standard identifier       "CD-I "
6       version                   1
8       system identifier         "CD-RTOS"
40      volume identifier         "CD-i Soccer"
84      volume space size         7,575 blocks
130     logical block size        2,048
136     path table size           216
148     path table location       LBA 2,269
190     volume set identifier     "CD-i Soccer"
318     publisher identifier      "Philips Interactive Media"
446     data preparer identifier  (blank)
574     application identifier    "CMDS/cdi_demo"
702     copyright file            "copyright"
739     abstract file             "abstract"
776     bibliographic file        "biblio"
813     creation date             1997052214560900
```

Sector 17 is the terminator (`0xFF`, `CD-I `, version 1) and the rest of it is
zero. There is no root directory record in the descriptor — CD-i does not have
one. The path table is the only way in.

The **application identifier is the boot path**: `CMDS/cdi_demo` is the file
the player loads and runs. It is also the first of several places where the
shipped disc is still wearing a working title (see
[11-leftovers.md](11-leftovers.md)).

The **data preparer field is blank**. Every other identifier is filled in.

## Path table, sector 2269

216 bytes, thirteen entries, alphabetical, every one of them a child of the
root:

```
   #  name              extent
   0  (root)            2270
   1  CELEB_GFX         7372        7  RTF               3202
   2  CMDS              3089        8  SAD_GFX           7268
   3  INTRO_GFX         5322        9  SAMPLES           5195
   4  PERM_GFX          5267       10  SCOREBOARD_GFX    7221
   5  PITCH_GFX         6227       11  TOURN_GFX         5633
   6  PLAYER_SPRTS      5921       12  TSELECT_GFX       5562
```

The volume is one level deep. Every directory hangs off the root; nothing
nests.

The path table is also present **as a file**: the root directory contains an
entry named `PATH_TBL` pointing at LBA 2269 with a length of 216 bytes and
attributes `0x0111` — readable by owner, group and world, executable by none,
not a directory. Nothing in the executable opens it. It is the authoring tool's
own copy of the table, exposed by accident.

## Directory records

Each record is the ISO 9660 layout up to the file identifier, then padded to an
even length, then ten bytes of CD-i system use:

```
+0x00  1   record length
+0x01  1   extended attribute length (always 0 here)
+0x02  8   extent LBA, both-endian; only the big-endian half is filled in
+0x0A  8   data length, both-endian; likewise
+0x12  6   date: year-1900, month, day, hour, minute, second
+0x18  1   GMT offset
+0x19  1   file flags
+0x1A  1   file unit size
+0x1B  1   interleave gap
+0x1C  4   volume sequence number, both-endian
+0x20  1   name length
+0x21  n   name
       .   one pad byte if n is even
       2   owner group id
       2   owner user id
       2   attributes
       2   reserved
       1   file number
       1   reserved
```

Every file on this disc has file unit size 0, interleave gap 0 and file number
1: nothing is an interleaved multi-channel real-time file at the *directory*
level, not even `/RTF/intro_anim`, whose interleaving lives in the sector
subheaders instead ([08-digital-video.md](08-digital-video.md)).

Attribute words take exactly two values:

| Value | Bits | Meaning |
|---|---|---|
| `0x0555` | 0, 2, 4, 6, 8, 10 | read + execute for owner, group and world — every file |
| `0x8111` | 0, 4, 8, 15 | read for owner, group and world; directory — every directory |
| `0x0111` | 0, 4, 8 | read only, no execute — `PATH_TBL` alone |

Every record has owner group 0, owner user 0, file flags 0, file unit size 0
and interleave gap 0. The file number is 1 for all 143 files and 0 for the
twelve directories and `PATH_TBL`. Nothing on this volume uses the extended
attribute record, and no record sets the hidden or associated-file flag.

## A name collision the disc does not mind and your host will

The root directory contains a **file** called `intro_gfx` and a **directory**
called `INTRO_GFX`. On CD-i these are two different names. On Windows, macOS
with the default file system, or any case-insensitive host, they are one, and a
naive extractor either fails or silently drops one of them.

`tools/cdifs.py extract` detects the clash and writes the file as
`intro_gfx.file`. If your own extraction produced 143 files instead of 144,
this is why.

The clash is not innocent. `intro_gfx` is a 320 × 224 Manchester United club
crest belonging to the abandoned asset set, which nothing opens; `INTRO_GFX/`
is the live logo directory the shipping game loads from. Two generations of the
same idea ended up in the same namespace.

## Reproducing

```
python tools/cdifs.py list          # every entry, disc order
python tools/cdifs.py tree          # hierarchy
python tools/cdifs.py map           # sector map with subheader flags
python tools/cdifs.py extract DIR   # write everything out
```
