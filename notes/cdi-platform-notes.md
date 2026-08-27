# CD-i platform notes — a checklist for the next disc

Written for a sibling pipeline documenting a *different* Philips CD-i title.
Everything here was learned on **Ultra CD-i Soccer (Europe)** and is split into
what should hold for any CD-i disc, what is worth testing because it *might*
hold, and what turned out to be specific to this one game.

The tools referenced live in [`../tools/`](../tools/). `cdilib.py`, `cdifs.py`,
`cdihead.py`, `os9mod.py`, `cdiaudio.py` and `cdirtf.py` are platform-general
and should work unmodified on another disc. `cdigfx.py`, `cdispr.py`,
`cdistrings.py` and `cditeams.py` carry title-specific tables and are worth
reading rather than running.

---

## 1. Open the image first, and open it raw

```
chdman extractcd -i "TITLE.chd" -o _work/disc.cue -ob _work/disc.bin
```

Expect a single `MODE2_RAW` track. **Do not** work from a cooked 2,048-byte
image: on CD-i the subheader is where the interleaving lives, and you lose it.

Sector layout, 2,352 bytes:

```
0..11    sync   00 FF FF FF FF FF FF FF FF FF FF 00
12..15   header MM SS FF mode, MSF in BCD, LBA + 150
16..23   subheader: file, channel, submode, coding -- stored twice
24..     user data: 2,048 (Form 1) or 2,324 (Form 2)
```

The Form bit is submode `0x20`. `cdilib.Disc.data()` sizes each sector from it;
anything that assumes 2,048 everywhere will silently corrupt real-time files.

Submode bits: `0x01` EOR, `0x02` video, `0x04` audio, `0x08` data, `0x10`
trigger, `0x20` Form 2, `0x40` real-time, `0x80` EOF.

---

## 2. Check the pre-file-system region — this is the highest-yield first move

**Run this before anything else.** On our disc it turned up 5.2 MB the game
never touches.

```
python tools/cdihead.py map
python tools/cdihead.py check
python tools/cdihead.py wav OUT/
```

The path table normally sits a long way in (LBA 2,269 here), and everything
before it belongs to nobody. Do not assume it is zeroes. Test, in this order:

1. **Is it plain zero?** Fine, move on.
2. **Is it the ECMA-130 scrambler sequence?** Generate the 2,340-byte LFSR
   stream (x^15 + x + 1, preset `$0001`, LSB first, reset per sector), take
   bytes 12.. to line up with Form 2 user data, and XOR. If it comes out zero,
   the region is *scrambled* zeroes.
3. **Does the XOR produce something structured?** On this disc, 1,203 sectors
   became 16-bit little-endian PCM.

Signals that a region is real audio rather than noise:

- `mean|x[n] - x[n-1]| / mean|x[n]|` well below 1 (0.12 here). Noise sits near 1.
- Left channel equal to right on every frame — mono content in a stereo
  container, which is what CD-DA of a mono source looks like.
- A harmonic series in the averaged FFT rather than a flat floor.

**Also compare the head against the tail.** Our tail padding was *plain* zeroes
while the head padding was *scrambled* zeroes. Two filler mechanisms in one
image means two different tools touched it, which is itself a finding.

If your disc's head region descrambles to audio too, **compare it with ours** —
same pressing run, same year, and a match would settle the open question in
[`../docs/12-open-questions.md`](../docs/12-open-questions.md) for both titles.
Our two clips are 7.41 s and 8.31 s at 44,100 Hz, fundamentals near 151 and
161 Hz.

---

## 3. The Green Book file system

Sector 16 is the volume descriptor. It is ISO 9660's skeleton with big-endian
numbers only, so **read the second half of every both-endian pair**.

```
1      "CD-I "        standard identifier
8      system id      expect "CD-RTOS"
40     volume id      <- often the working title, not the box title
84     volume space size (blocks)
130    logical block size
136    path table size
148    path table LBA
190    volume set id
318    publisher
446    data preparer  <- frequently blank
574    application id <- THE BOOT PATH, e.g. "CMDS/cdi_demo"
702/739/776  copyright / abstract / bibliographic file names
813    creation date, YYYYMMDDHHMMSSss
```

Two things to grab immediately:

- **The application identifier is the executable's path.** Compare it with the
  title on the box and with the OS-9 module name inside the file. On our disc
  all three disagreed.
- **`abstract` and `biblio`, if named, are plain text on the disc.** Ours held
  the marketing copy and the *complete credits* — the only place several names
  appear. Always `cat` them.

There is **no root directory record in the descriptor**. CD-i reaches the root
through the path table only, and the root extent's own `.` record carries the
true directory length. `cdilib.walk()` handles this.

Directory records are ISO 9660 up to the name, padded to even, then **ten bytes
of system use**: owner group (2), owner user (2), attributes (2), reserved (2),
file number (1), reserved (1).

Attribute bits: 0 owner-read, 2 owner-exec, 4 group-read, 6 group-exec,
8 world-read, 10 world-exec, 12 CDDA, 15 directory. Expect `0x0555` for files
and `0x8111` for directories; anything else is worth a look (ours flagged the
path table exposed as a file).

**Watch for case collisions when extracting.** We had a root file `intro_gfx`
and a root directory `INTRO_GFX`; on Windows or macOS a naive extractor drops
one. `cdifs.py extract` detects this and suffixes the loser `.file`. If your
extracted file count is one short of the directory listing, that is why.

---

## 4. Census the disc before reading any of it

Three cheap passes that pay for themselves:

```
python tools/cdifs.py list    # LBA, size, date, attributes
python tools/cdifs.py map     # who owns each sector, with submode flags
```

- **All-zero files.** `collections.Counter(bytes)` per file. Ours found sixteen
  totalling 1,070,080 bytes — an entire abandoned localisation. This takes ten
  seconds and is the single best leftover-hunting move on a CD-i disc, because
  the format has no space pressure to force anyone to delete them.
- **Directory dates.** Every record has a six-byte date. Bucket them by month:
  the shape of the schedule falls out, and files whose dates cluster far from
  everything else are usually a different generation of the same assets. Our
  directories all carried the mastering timestamp, so only *file* dates mean
  anything.
- **Gaps in the sector map.** Anything owned by `<free>` inside the file area
  deserves a hexdump.

---

## 5. The executable is one or more OS-9/68000 modules

```
python tools/os9mod.py _work/files/CMDS/<name>
```

Modules start with `$4AFC` and are self-validating, so you can find them by
scanning and confirm them by arithmetic:

```
0   $4AFC sync         18  type      1=Prgrm 2=Sbrtn 3=Multi 4=Data
2   M$SysRev                         $B=Trap $C=Systm $D=FlMgr $E=Drivr $F=Devic
4   M$Size              19  lang     1 = 68000 object
8   M$Owner             20  attr     bit7 re-entrant, bit5 sticky
12  M$Name (offset)     21  revision
16  M$Accs              46  M$Parity = ~(XOR of the 24 header words)
48  M$Exec  52 M$Excpt  56 M$Mem  60 M$Stack
64  M$IData 68 M$IRefs  72 M$Init 76 M$Term
```

Module CRC is a 24-bit poly `$800063`, preset `$FFFFFF`, and running it over the
**whole** module including the stored CRC must give `$800FE3`. If it does, the
binary has not been patched since the link — worth stating.

Names are NUL-terminated here, not high-bit-terminated as classic OS-9 docs
describe. Handle both.

A second, tiny module of type `$B` (Trap) next to the main program is normal:
it is the shared-library / trap-handler mechanism. Ours was 370 bytes with init
and termination routines and a `line_event` string beside it.

**Look at the bytes immediately after the 80-byte header.** Ours were not code
but a 29-glyph 1bpp 8×8 font — the alphabet the loader error screens need
before any file has been read. A cut-down character set linked ahead of the code
is a good tell for "this is drawn before the file system is up".

---

## 6. Strings, and the trick that pays best

68000 object code produces enormous amounts of accidental ASCII, so filter:
keep runs that are mostly letters and whose words are long enough to be
language. `cdistrings.py` does this and separates disc paths from prose.

Then do the thing that found most of our archaeology:

> **Cross-reference every path-shaped string against the directory listing, in
> both directions.**

- Paths in the binary that resolve to nothing = features cut late, with their
  original names intact. Ours gave `/segalogo_gfx`, `/comment_gfx`,
  `/ocean6a_gfx`, `/tmsplng_gfx`, `/kit1_rlspr` — the last of which *named an
  undocumented file format*.
- Files on the disc that the binary never names = dead weight, usually an
  earlier generation of assets.

The path strings usually sit in **load order**, which is free information about
program flow, and a missing name's neighbours tell you which screen it belonged
to.

Other things to grep for by hand once the filter has run: profanity and
`debug`/`test`/`cheat` (ours had `CHEAT MODE ON` and an unprintable error
message), `TV`/`MONITOR`/`WINDOW` (development-host options), and placeholder
prose — look specifically *between* legitimate string blocks, which is where
ours hid a copyright notice nobody replaced.

---

## 7. Graphics

Assume raw and uncompressed until proved otherwise. On CD-i the MCD212 reads
CLUT planes straight out of memory, so a file is very often a framebuffer.

**Palettes** are flat RGB triplets. The size tells you the mode:

```
192 bytes = 64 entries  = 1 CLUT bank
384 bytes = 128 entries = 2 banks   (CLUT7)
768 bytes = 256 entries = 4 banks   (CLUT8)
```

Entry 0 is the transparency key — `#00FF00` on almost everything we saw.

**Finding dimensions.** Take `max(pixel value)` first: a ceiling of 127 means
CLUT7, 63 or 31 means a smaller bank. Then try widths in this order:

```
384   CD-i normal resolution
512   power-of-two line pitch -- see below
280 / 240 as heights (PAL / NTSC full screen: 107,520 and 92,160 bytes)
320   NOT a CD-i size; if this is what renders, the art came from elsewhere
```

**The 512-byte line pitch caught us out and will catch you out.** Two
122,880-byte files were 384 pixels of picture inside a 512-byte line, with 128
columns of filler on the right. Rendered at 384 they shear into diagonal noise
that looks like a compression format. If a file size is not a multiple of 384
but *is* a multiple of 512, try 512 before you start writing a decompressor.
Scrolling playfields may use the whole 512 (our pitches were 512 × 768).

**If a file renders at 320 × 224, stop and take it seriously.** That is a Mega
Drive PAL frame, not a CD-i one, and on our disc it was one end of a chain
(orphan 320 × 224 art → a `/segalogo_gfx` reference → Cross Products in the
thanks list) pointing at a Sega-era toolchain and an earlier version of the
game. Other non-CD-i sizes deserve the same attention.

**Sprites.** Ours used a format the binary called `rlspr`: a flat array of
fixed-size slots, each holding run-length-coded lines.

```
0x00..0x7F   one pixel of that index
0x80..0xFD   skip (n & 0x7F) transparent pixels
0xFF         end of line
0xFE         filler, pads the slot to its fixed size
```

Recognise it by pixel values above `0x80` in a file whose palette has 128
entries, and find the slot size by counting runs of the filler byte: our bank
had 416 filler runs in 53,248 bytes, so slots were 128 bytes. Do not assume the
`_sprts` suffix means coded — on our disc most `_sprts` files were plain
bitmaps.

**Fonts** appeared in three layouts on one disc, so test all of them: glyph-major
fixed cells, a **single strip N pixels tall** (glyph *n* is a vertical slice —
this is why 16 × 16 cells produce recognisable-but-sheared letters), and 1bpp
packed rows for anything linked into the executable. Read the character set once
you have it: ours was IBM CP437 `0x20`–`0xAA`, which dates the art pipeline to a
PC even though the console is a 68000 running OS-9.

---

## 8. Audio

Expect **Green Book ADPCM**, and expect it wrapped:

- Ours shipped as **AIFF-C** (`FORM`/`AIFF`) with the samples in a non-standard
  **`APCM`** chunk instead of `SSND`, with the same 8-byte offset/blocksize
  preamble. `COMM` is honest about channels, bits and rate.
- Sample rate is an 80-bit IEEE extended float. **18,900 Hz** = Level C,
  **37,800 Hz** = Level A or B; 4 bits/sample = Level B or C, 8 bits = Level A.

`cdiaudio.py` decodes Level B/C. The 128-byte sound group is 16 parameter bytes
plus eight 28-sample units (224 samples). Confirm the header layout rather than
assuming it — the sixteen bytes are eight parameters stored twice, and checking
which halves match tells you which is which:

```
bytes 0-3 == 4-7 and 8-11 == 12-15   -> units 0-3 from 0-3, units 4-7 from 8-11
```

Data byte `16 + t*4 + (u & 3)`, low nibble for units 0–3 and high nibble for
4–7. Predictor coefficients `f0 = 0, 60, 115, 98, 122`, `f1 = 0, 0, -52, -55, -60`,
shifted right 6.

**Read the extra chunks.** Three of our twelve files carried `MARK`, `INST` and
a 424-byte `APPL` whose signature was `Sd2a` — Digidesign Sound Designer II —
and their dates were three weeks later than the other nine. Authoring-tool
fingerprints in an audio container are free provenance.

**Check whether the music actually ships.** Ours has a 21-entry sound test
naming eight tunes and no file on the disc holds one. Enumerate the sound-test
strings and map them onto the audio files; a shortfall is a real finding.

---

## 9. Real-time files and Digital Video

Anything under `/RTF` — or any file whose sectors have submode bit `0x40` set —
must be read **by sector, not through the directory record**. The size in the
directory entry is a Form 1 fiction.

```
python tools/cdirtf.py map      # census by (file, channel, submode, coding)
python tools/cdirtf.py demux OUT.mpg
python tools/cdirtf.py info
```

Adjust `START` and `COUNT` in `cdirtf.py` to your file's LBA and sector count.

Sectors tagged neither VIDEO nor AUDIO are **bitrate padding** and carry
nothing — 19.5 % of ours. Drop them; concatenate the rest at 2,324 bytes each.

If the payload starts `00 00 01 BA`, it is an MPEG-1 system stream and the title
needs the **Digital Video cartridge**. Confirm by looking for the refusal screen:
grep the executable for `CARTRIDGE` and look for a large root-level bitmap named
something like `nodv_gfx`. Sequence header (`00 00 01 B3`) gives resolution and
rate; expect **368 × 272** at 25 fps for PAL CD-i DV, which is *not* the
352 × 288 of Video CD.

---

## 10. Baseline, so you can tell signal from noise

What our disc looked like, for comparison:

| | Ultra CD-i Soccer |
|---|---|
| Track | one, MODE2_RAW, 7,875 sectors (1 min 45 s), 2.4 % of a CD |
| Entries | 12 directories, 144 files, 10,635,729 bytes, one level deep |
| Pre-FS region | 2,269 sectors, scrambled, 28.5 % of the image |
| Executable | 229,376 bytes, two OS-9 modules |
| Compression | none, anywhere, except the run-length sprites |
| Palettes | 192 / 384 / 768 bytes, entry 0 = `#00FF00` |
| Audio | 12 effects, 10.2 s total, Level C ADPCM in AIFF-C |
| Video | 4,079,616-byte RTF, MPEG-1 368 × 272 |
| All-zero files | 16, totalling 1,070,080 bytes |
| Dangling path references | 8 |

If your disc compresses something, uses interleaved multi-channel real-time
files, or has more than one directory level, it is doing something ours did not
and that is worth a page of its own.

---

## 11. Order of work that worked

1. `chdman extractcd`, confirm one MODE2_RAW track.
2. `cdihead.py map` — the pre-file-system region, before anything else.
3. Volume descriptor and path table; note the application identifier.
4. `cdifs.py list` / `map` / `extract`; all-zero census; date histogram.
5. `cat` the copyright / abstract / bibliographic files.
6. `os9mod.py` on the boot file; check parity and CRC; look at the first bytes
   after the header.
7. Filtered strings; then the two-way path cross-reference.
8. Palette sizes → pixel-value ceilings → widths, and render everything.
9. Audio containers and their extra chunks.
10. Real-time files last — they are big, and by then you know the conventions.

Write down what does *not* resolve. Half of what makes a disc interesting is
the list of things that are measurably odd and not yet explained.
