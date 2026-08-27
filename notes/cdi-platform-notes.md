# CD-i platform notes — moved

This checklist is no longer kept in this repository. The canonical copy lives
in one of its own, so that every CD-i pipeline reads and extends **the same
document** instead of carrying a fork that quietly drifts away from the others:

→ **[cdi-platformnotes-doc](https://github.com/vs-sr-dev/cdi-platformnotes-doc)**

## Why

Three pipelines each carried a copy and each extended it, and the copies had
already begun to contradict one another. Two examples, both now fixed in the
merged document:

- The audio coding byte `0x01` was documented as CD-i **Level A** in one copy
  and **Level B stereo** in another. It is Level B stereo — Level A is the
  8-bit one, `0x10`/`0x11` — and getting it wrong costs a factor of two in
  every duration you compute.
- The byte loss in the pre-file-system audio was recorded as six stereo frames
  (24 bytes) per sector in one copy. Measured per channel on a third disc it is
  **seven frames, 28 bytes** — the extra four being the EDC field, which the
  authoring system zeroes.

A per-pipeline copy is a reliable way of preserving the older of two answers.

## What this disc contributed

*Ultra CD-i Soccer* started the checklist and supplies most of its section 1
to 8: the scrambler test for the pre-file-system region, the two filler
mechanisms, Green Book directory attributes and the case-collision trap, the
all-zero-file census, OS-9 module parity and CRC, the two-way path
cross-reference, the 512-byte line pitch that shears a bitmap into what looks
like a compression format, the `rlspr` sprite layout, the three font layouts,
AIFF-C with an `APCM` chunk, and Digital Video detection.

It also supplies the low end of the baseline: a disc using **2.4 %** of a CD,
compressing nothing, where the program owns every asset it draws.

## What is in the merged document

The sector and Green Book layouts, the scrambler test for the pre-file-system
region and the mechanism behind it, OS-9/68000 module validation and toolchain
fingerprints, scanning an executable for a symbol table, the subheader coding
bytes, DYUV, proving a bitmap geometry to the byte, run-length codings and
fixed frame slots, the ADPCM sound-group layout, multi-channel real-time
interleave, tagged chunks and code hiding inside data — and a baseline table
putting all three discs side by side so you can tell what is normal for CD-i
from what your title is doing differently.

Findings confirmed on every disc are marked `[all]`; those confirmed on two are
marked `[2 of 3]`. Everything else is named after the disc it came from, and is
the kind of thing to test rather than assume.

## Contributing

Findings about the **format** go to the shared document. Findings about **this
title** stay in this repository. Mark something `[all]` only after actually
checking the other discs, and when you correct something, fix it in place and
say so — the corrections are more useful with their history attached.
