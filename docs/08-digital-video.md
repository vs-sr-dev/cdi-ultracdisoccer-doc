# 08 — Digital Video

`/RTF/intro_anim` is 4,079,616 bytes — 38 % of everything in the file system,
and more than the game, the pitches, the players and the sound put together.

## Why the cartridge is mandatory

The base CD-i player has no video decoder. MPEG playback was sold as an add-on,
the **Digital Video cartridge**, and a title that used it had to cope with
players that did not have one. Most such titles degraded gracefully. This one
does not: it ships a full-screen refusal.

```
0x05B0E           YOU DO NOT HAVE YOUR
              DIGITAL VIDEO CARTRIDGE LOADED
              PLEASE SWITCH OFF YOUR CDI PLAYER
              INSERT THE CARTRIDGE AND RESTART.
               IF YOU DO NOT HAVE A CARTRIDGE
                    PLEASE CONTACT YOUR
              LOCAL CDI SUPPLIER FOR DETAILS.
```

and a 122,880-byte picture, `/nodv_gfx`, to say it on — the Philips Media
logo with a red exclamation mark, 384 pixels of picture in a 512-byte line
([04-graphics.md](04-graphics.md)), with a 256-entry palette all of its own.
"nodv" is "no DV".

Two of the largest root-level files on the disc exist to tell you the disc will
not run.

## A real-time file is not a byte stream

The directory entry says 4,079,616 bytes at LBA 3203. Read it the way you read
every other file — 2,048 bytes of Form 1 user data per sector — and you get
garbage, because the sectors are **Form 2** and carry 2,324 bytes each, and
because a fifth of them carry nothing at all.

```
python tools/cdirtf.py map

file chan submode  flags                    coding  sectors
   1    0    0x60  RT|F2                      0x00      388
   1    0    0x62  RT|F2|VIDEO                0x0f     1027
   1    0    0x64  RT|F2|AUDIO                0x7f      576
   1    0    0xe5  EOF|RT|F2|AUDIO|EOR        0x7f        1

1992 sectors, 388 of them bitrate padding (19.5%), 4,629,408 bytes raw
```

Every sector sets the real-time bit. 1,027 are tagged video, 577 audio, and
**388 are tagged neither** — they are padding, inserted so the drive delivers a
constant bit rate to the decoder no matter how the compressor's output varies.
Read as a flat file they are 900 KB of noise in the middle of the stream; read
as a real-time file they are silence.

Dropping them leaves 3,727,696 bytes of MPEG-1 system stream.

## What is in the stream

```
python tools/cdirtf.py info

demuxed 3,727,696 bytes
sequence header @0x948: 368x272  25 fps  aspect 1.0695  1,180,000 bit/s
audio PES 0xc0 first at 0x22
MPEG audio @0x5dc9d: layer II  48000 Hz  160 kbit/s  mode mono
```

| | |
|---|---|
| Container | MPEG-1 system stream, pack headers every sector |
| Video | MPEG-1, **368 × 272**, 25 fps, 1.18 Mbit/s, pixel aspect 1.0695 |
| Audio | MPEG-1 Layer II, 48 kHz, **160 kbit/s, mono** |
| Duration | ~22 s at the declared rates |

368 × 272 is the CD-i Digital Video frame, not the 352 × 288 of Video CD: the
cartridge decodes to a 384-wide CD-i plane and the extra sixteen columns are
overscan. 25 fps and 272 lines put it firmly on the PAL side, which matches a
European release with a 280-line credits backdrop in `INTRO_GFX`.

The audio is **mono at 160 kbit/s** — a stereo-grade bitrate spent on one
channel. Whoever encoded it did not change the default.

```
python tools/cdirtf.py demux intro.mpg
```

writes a file most players will open.

## Who made it

`biblio` credits **Dave Colledge** with the intro sequence and **John Avery**
with "Intro Music and Sound Effects". The in-game credit roll says the same:
`Intro Animation  DAVE COLLEDGE`.

The still frames that surround the film are in `INTRO_GFX`, and their dates
bracket it: `philbump` (the Philips Media bumper) 1996-11-29, `krislogo`
(the Krisalis logo, "Written and produced by Krisalis Software LTD")
1997-01-23, `credback` 1997-02-06, `logo_gfx` (the **CD-i SOCCER** title)
1997-02-05. The real-time file itself is stamped 1997-05-22 with the rest of
the mastering pass, so its own date says nothing.
