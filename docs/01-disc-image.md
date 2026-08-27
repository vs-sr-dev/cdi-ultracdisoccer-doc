# 01 — The disc image

## One track, and it is not what the file system says

The CHD carries a single track:

```
TRACK:1  TYPE:MODE2_RAW  FRAMES:7875  PREGAP:0
```

7,875 sectors of 2,352 bytes. Every sector has a correct twelve-byte sync
pattern, a correct binary-coded MSF header, and a subheader stored twice, as
Green Book requires. `tools/cdihead.py check` verifies all three across the
first 2,269 sectors and finds nothing wrong.

What the file system claims is a smaller disc. The volume descriptor says
7,575 blocks, and the last file ends at sector 7,537. Between the two figures
sits a gap at each end of the disc — and the gap at the *front* is 5.2 MB.

## The sector map

`tools/cdifs.py map` walks every sector and prints who owns it and what its
subheader says. Collapsed:

| Sectors | Count | Form | Owner |
|---|---:|---|---|
| 0 – 15 | 16 | 2 | not in the file system |
| 16 – 17 | 2 | 1 | CD-i volume descriptor, then the terminator |
| 18 – 2268 | 2,251 | 2 | not in the file system |
| 2269 | 1 | 1 | `/PATH_TBL` — the path table, also exposed as a file |
| 2270 – 2271 | 2 | 1 | the root directory extent |
| 2272 – 7537 | 5,266 | 1 | the files |
| 7538 – 7874 | 337 | 2 | zero padding to the end of the track |

The tail is exactly what you expect: 337 Form 2 sectors of plain zeroes with a
correct EOF flag on the first of them.

The head is not.

## 2,269 sectors of scrambled data in front of the file system

Sectors 0–2268 are well-formed Mode 2 Form 2 sectors whose 2,324-byte user
data is high-entropy noise — 7.9 bits per byte, no ASCII, no structure. 1,064
of them are byte-identical to each other, which is the tell: a repeating
2,324-byte pseudorandom block is what you get from the **ECMA-130 Annex B
scrambler** running over zeroes.

The scrambler is a 15-bit LFSR over x^15 + x + 1, preset to $0001, clocked LSB
first, producing 2,340 bytes per sector and reset at every sector boundary.
Line the sequence up against the Form 2 user area — that is, start at scrambler
offset 12 — and XOR:

```python
python tools/cdihead.py map
    0-15       16 sectors     37,184 B  scrambled zeroes
   16-17        2 sectors      4,648 B  volume descriptor
   18-584     567 sectors  1,317,708 B  scrambled PCM
  585-1632   1048 sectors  2,435,552 B  scrambled zeroes
 1633-2268    636 sectors  1,478,064 B  scrambled PCM
```

1,064 sectors descramble to nothing but zeroes. The other 1,203 descramble to
**16-bit signed little-endian PCM**.

## What the descrambled audio is

Two runs, 7.41 s and 8.31 s at 44,100 Hz:

| | run 1 | run 2 |
|---|---|---|
| sectors | 18 – 584 | 1633 – 2268 |
| frames | 326,592 | 366,336 |
| left channel == right channel | 326,592 / 326,592 | 366,336 / 366,336 |
| mean abs sample | 2,066 | 2,074 |
| mean abs first difference | 265 | 246 |
| spectral centroid | 2,740 Hz | 2,673 Hz |
| strongest partials | 151, 161, 334, 345, 377 Hz | 151, 161, 366, 377, 355 Hz |

Both channels are identical for every single frame, so this is mono content in
a stereo container. The ratio of mean |dx| to mean |x| is 0.12 — a smooth
waveform, not noise. The spectrum is a harmonic series over a fundamental near
155 Hz. The two runs do not correlate with each other (peak normalised
cross-correlation 0.046) and neither is a loop of itself, so they are two
different pieces of audio, not one clip stored twice.

`tools/cdihead.py wav _work/headwav` writes them out.

## What it means, and what it does not

The measurements above are solid. The interpretation is not, and this
repository does not pretend otherwise.

What can be said: the sectors were **written already scrambled**. Their EDC
words check out over the scrambled bytes, so the scrambling was applied to the
content before it was placed into the sector, not by the pressing plant on top
of a finished sector. A drive returning these sectors in cooked mode hands the
player noise, and the file system does not name a single byte of this region:
every path string in `cdi_demo` resolves to a directory entry or to the
player's NVRAM device (see [11-leftovers.md](11-leftovers.md)).

What that looks like is filler: a mastering step that needed 2,269 sectors of
something in front of the file system and pulled it out of whatever buffer was
to hand — a buffer that happened to hold the raw, still-scrambled data track of
another disc, one carrying a mono audio programme. The two zero runs and the
two audio runs alternate exactly as a partially-overwritten buffer would.

The contrast with the tail is the strongest hint. The 337 sectors *after* the
files are plain zeroes, written by something that knew to write zeroes. The
1,064 zero sectors in front are *scrambled* zeroes, written by something that
did not. Two different filler mechanisms in one image says the front region did
not come from the same step as the rest.

Identifying the audio itself is [open](12-open-questions.md).

## Where the space went

| | sectors | bytes | share |
|---|---:|---:|---:|
| pre-file-system region | 2,269 | 5,273,156 | 28.5 % |
| file system and files | 5,269 | 10,790,912 | 58.3 % |
| tail padding | 337 | 783,188 | 4.2 % |
| ECC/EDC and headers | — | 1,674,744 | 9.0 % |

Nearly a third of a disc that is itself 2.4 % full is occupied by something the
game never reads.
