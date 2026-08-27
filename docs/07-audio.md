# 07 — Audio

Twelve sound effects, 128,778 bytes, in `/SAMPLES`. That is the entire audio
budget outside the intro film — 1.2 % of the bytes in the file system, against
18 % for the five pitch bitmaps.

## AIFF-C with a chunk that is not in the spec

Every effect opens `FORM … AIFF`. They are Apple audio files, which on a
Philips console running OS-9 is already worth a note — the sound was cut on a
Macintosh. What follows the `COMM` chunk is not `SSND`:

```
python tools/cdiaudio.py info

file                    bytes   frames    rate ch bits  groups seconds  chunks
curs_move_sfx            2358     1338   18900  1    4      18    0.07  COMM(18) APCM(2312)
curs_select_sfx          2358     2618   18900  1    4      18    0.14  COMM(18) APCM(2312)
error1_sfx               4662     4463   18900  1    4      36    0.24  COMM(18) APCM(4616)
error2_sfx               2358     1511   18900  1    4      18    0.08  COMM(18) APCM(2312)
foul_sfx                11574    16401   18900  1    4      90    0.87  COMM(18) APCM(11528)
goalcheer_sfx           23564    38272   18900  1    4     180    2.02  COMM(18) APCM(23048) MARK(2) INST(20) APPL(424)
hitpost_sfx              2358     1350   18900  1    4      18    0.07  COMM(18) APCM(2312)
kick_sfx                 2358     1657   18900  1    4      18    0.09  COMM(18) APCM(2312)
nearmiss1_sfx           16652    25216   18900  1    4     126    1.33  COMM(18) APCM(16136) MARK(2) INST(20) APPL(424)
nearmiss2_sfx           23564    39808   18900  1    4     180    2.11  COMM(18) APCM(23048) MARK(2) INST(20) APPL(424)
whistle_long_sfx        32310    53516   18900  1    4     252    2.83  COMM(18) APCM(32264)
whistle_short_sfx        4662     5118   18900  1    4      36    0.27  COMM(18) APCM(4616)
```

`APCM` — ADPCM — holds the sample data with the same eight-byte offset and
block-size preamble a real `SSND` chunk would have. The `COMM` chunk is
honest: one channel, four bits per sample, and a sample rate stored as an
80-bit IEEE extended float that decodes to exactly **18,900 Hz**.

Four bits at 18.9 kHz mono is **CD-i ADPCM Level C**, the lowest of the three
Green Book audio levels: sixteen mono channels can share a disc at that rate,
and one second costs 9,450 bytes.

Total playing time of every sound in the game: **10.2 seconds**.

## The Level B/C sound group

The ADPCM payload is a run of 128-byte **sound groups**. Each is sixteen
parameter bytes followed by 112 data bytes carrying eight **sound units** of 28
samples — 224 samples per group, and 18 groups — 4,032 samples — fill one Form 2
sector's user area exactly.

The sixteen parameter bytes are eight parameters stored twice, which is how the
layout can be confirmed rather than guessed. Across all 252 groups of
`whistle_long_sfx`:

```
bytes 0-3 == bytes 4-7  and  bytes 8-11 == bytes 12-15   in 252 of 252 groups
bytes 0-3 == bytes 8-11                                  in  13 of 252
```

So units 0–3 take their parameter from bytes 0–3 and units 4–7 from bytes 8–11,
with 4–7 and 12–15 the redundant copies the Green Book asks for. Each parameter
byte is a filter index in the high nibble and a range (right shift) in the low
nibble. This disc uses ranges 1 through 12 and filters 0, 1 and 3 — filter 2 is
never chosen, filter 4 never appears.

Data byte `16 + t*4 + (u & 3)` carries unit `u` in its low nibble for u < 4 and
in its high nibble for u ≥ 4, so the 28 samples of four units interleave down
the group. Decoding is the usual second-order predictor:

```
s = sign_extend_4(nibble)
v = (s << 12) >> range
v += (f0[filter] * prev1 + f1[filter] * prev2) >> 6
```

with `f0 = 0, 60, 115, 98, 122` and `f1 = 0, 0, -52, -55, -60`.

`tools/cdiaudio.py wav OUTDIR` decodes all twelve to 16-bit WAV.

## Padding tells you the block size

Every file's `APCM` chunk is a whole number of groups, and the group count is
always a multiple of 18 — 18, 36, 90, 126, 180, 252 — which is 2,304 bytes, one
Form 2 sector's user area. The samples the `COMM` chunk declares stop well
short of that: `kick_sfx` is 1,657 samples in a slot that holds 4,032. The
tool that produced these rounded every effect up to the sector.

## Three files came from somewhere else

`goalcheer_sfx`, `nearmiss1_sfx` and `nearmiss2_sfx` carry three chunks the
other nine do not: `MARK`, `INST`, and a 424-byte `APPL`. The `APPL` chunk's
four-byte application signature is:

```
53 64 32 61     "Sd2a"
```

and inside it, in plain text:

```
SampSize   8 bit   16 bit   24 bit
```

`Sd2a` is **Digidesign Sound Designer II**. Those three files went through a
Sound Designer session and kept its settings block; the other nine did not.

The dates agree. The nine plain files are stamped 1996-09-11 to 1996-09-17; the
three Sound Designer files are stamped 1996-10-02 17:18–17:19, three weeks
later, within ninety seconds of one another. They are the crowd: a goal cheer
and two near-misses, the three longest sounds in the game, redone in a proper
editor after the rest were done.

## Where the music is not

The executable carries a sound-test menu with 21 entries
([notes/string-inventory.md](../notes/string-inventory.md)):

```
BLANK (MUSICOFF)  TITLE THEME  WIN EUROPEAN CUP  WIN CUSTOM  WIN LEAGUE
CREDITS  LOSE LEAGUE  LOSE CUP  INGAME CROWD  CROWD FX 1..4
CHEER 1  KICK 1  PLAYER FOULED  CROSSBAR  SHORT REF  LONG REF  VALID  INVALID
```

The bottom eight map cleanly onto the twelve files in `/SAMPLES`. The top eight
— every piece of *music* the game names, including the title theme and the
credits music — have no file on this disc. `MUSIC` is an option on the sound
menu; `TEST TUNE` is a menu item.

The only music that demonstrably ships is the MPEG audio track inside the intro
film ([08-digital-video.md](08-digital-video.md)), and the `biblio` file credits
**John Avery** with "Intro Music and Sound Effects" — intro music, singular.

Whether the eight tunes were cut, or live somewhere this analysis has not
found, is [open](12-open-questions.md). The 15.7 seconds of mono PCM sitting in
front of the file system ([01-disc-image.md](01-disc-image.md)) is the obvious
place to look and does not obviously fit: it is 44.1 kHz where everything else
on the disc is 18.9 or 48 kHz, and the game has no code path that could reach
it.
