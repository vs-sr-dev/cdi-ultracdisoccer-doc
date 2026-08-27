# 12 — Open questions

Everything here is unresolved, with the measurement that makes it a question.

## What is the audio in front of the file system?

Sectors 18–584 and 1633–2268 descramble to 7.41 s and 8.31 s of 16-bit PCM at
44,100 Hz, mono content in a stereo container (left equals right in all 692,928
frames), harmonic, fundamental near 155 Hz, the two clips uncorrelated with each
other. Details in [01-disc-image.md](01-disc-image.md).

What is not known: what the music or sound is, and how it got there. Three
readings, none of them settled:

1. **Mastering filler.** The likeliest. A tool needed 2,269 sectors of
   something and used a buffer that still held another disc's raw, unscrambled
   data track. Supported by the fact that the 1,064 zero sectors in this region
   are *scrambled* zeroes while the 337 zero sectors at the end of the disc are
   plain — two different filler mechanisms, so two different steps.
2. **The missing music.** The executable names eight tunes that have no file
   ([07-audio.md](07-audio.md)). Against it: everything else in the game is
   18,900 Hz or 48,000 Hz, not 44,100; the audio is outside the file system;
   and 15.7 s across two clips does not cover eight cues.
3. **A CD-i Ready artefact.** Some CD-i discs hide data in an audio track's
   pregap. This disc has no audio track and no pregap, so the layout does not
   match; but a mastering chain that supported the format might explain a
   scrambled audio buffer being in the tool's hands at all.

Anyone with a second CD-i disc from the same 1997 Philips pressing run could
settle this in an afternoon by descrambling its own pre-file-system region and
comparing.

## Where is the music?

`BLANK (MUSICOFF)`, `TITLE THEME`, `WIN EUROPEAN CUP`, `WIN CUSTOM`,
`WIN LEAGUE`, `CREDITS`, `LOSE LEAGUE`, `LOSE CUP` are entries in the sound
test. `MUSIC` is a toggle on the options menu; `TEST TUNE` is a menu item. No
file on this disc holds a tune, and the twelve `/SAMPLES` files account for the
other thirteen sound-test entries exactly.

Either the music was cut and the menu entries left behind, or it is synthesised
by code, or it is somewhere unexamined. A disassembly of what `TEST TUNE`
dispatches to would answer it.

## What are the nine player ratings?

Nine bytes per player, 0–100, no labels anywhere in the strings. The
`Player STATS` screen draws them with the Tacti-Grid font rather than with a
text label per row, so the names are in the artwork, not in the binary.

`notes/team-database.md` has all 1,454 rows if you want to correlate them
against players you know.

## What do the other player flag bits mean?

```
bit 7   1,433 of 1,454   set on everything except the joke team
bit 5     154            selects a darker sprite (strong but imperfect correlation)
bit 1     488
bit 0      88
```

Bits 0 and 1 have no reading. 488 out of 1,454 is 34 %, which is about the rate
of left-footedness in professional football, but that is a coincidence until
somebody checks it against players whose stronger foot is known.

## What are the top four nibbles of the kit field?

Six bytes at team `+0x038`. The bottom eight nibbles behave like colour
indices; nibble 0 is always 1, nibble 1 is 1–6, nibbles 2–3 are 9 in 57 and 46
of 75 records respectively. Neither of those is a colour.

## What layout is `PITCH_GFX/t4font_sprts`?

16,640 bytes, pixel values 0–63, eighteen distinct. Not glyph-major at 8 × 8,
not a 16-line strip, not `rlspr` (nothing exceeds `0x3F`). Every rectangular
factorisation renders as noise, which usually means a header.

## What layout is `TSELECT_GFX/eng_tglass_gfx`?

46,754 bytes — not divisible by 2, 4, 8, 16, 32 or any plausible width — with
pixel values 0–31. Every other picture on this disc is a whole number of rows
of a whole number of pixels. This one is not, so it is either compressed or
carries a header and a payload. It is the "glass" overlay on the team select
screen; `tglass_pal` is a normal 128-entry palette.

## Where is `propfont`'s width table?

`PERM_GFX/propfont` is a proportional face stored as a 1,456 × 16 strip with no
widths in the file. They must be a table in `cdi_demo`, and 91 or so bytes of
small integers is a hard thing to find by inspection.

## Which CLUT do the player sprites land in?

`PLAYER_SPRTS` has no palette file. The kit banks use 45–49 distinct indices
each and colour is baked in, so the ten kits are ten fixed colour schemes — but
which bank of which CLUT the indices address is not established.
`tools/cdispr.py` renders against `PITCH_GFX/nmlpitch_pal` because that is the
CLUT loaded during a match, and the results are plausible rather than proven.

## Is `celeb_pal` broken?

64 entries, 15 distinct colours arranged as a 16-entry block repeated four
times, against a 245,760-byte picture using indices 0–31. Rendered together,
the celebration screen is two colours. Either the game overrides the CLUT at
run time or this palette shipped unfinished.

## What is `/ocean6a_gfx`?

A path in the load table pointing at a file that does not exist, with a
matching `_pal`. The name is not a screen, a team or a competition. Nothing
else on the disc uses `ocean`.

## What is the 588-byte structure at `0x1A4B8`?

Two records, 588 bytes apart, seeded with `ROTHERHAM UNITED` and
`MANCHESTER UNITED` and carrying `0xC350` (50,000) twice and `0xCAAC` (51,884)
in fixed positions. It sits between the team blurb and the team database. Best
guess is a Custom League default or a saved-state template.

## What does `cdi_syst` actually do?

370 bytes, OS-9 trap module, sticky, with init and termination routines,
referenced from module 1 next to the string `line_event`. Small enough to read
in an afternoon with a 68000 disassembler, and nobody has.
