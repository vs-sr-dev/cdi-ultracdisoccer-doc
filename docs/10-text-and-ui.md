# 10 — Text and the user interface

All of the game's text is uncompressed ASCII in `cdi_demo`, in four clusters.
The full extraction is in
[notes/string-inventory.md](../notes/string-inventory.md); this page is what it
tells you about the game.

## The shape of the game

```
COMPETITION         Instant Action   Head To Head   League Ladder
                    Custom League    Champions Cup  Champions League
OPTIONS             PASSWORD  MATCH LENGTH  ISO CONTROL  REDEFINE KEYS
                    TEST TUNE  TEST SFX  CANCEL
MATCH LENGTH        4 MINUTES  7 MINUTES  10 MINUTES
ISO CONTROL         NORMAL  ROTATED
GAME OPTIONS        SOUND  MUSIC  WEATHER  COMMENTARY  REFEREE  CONTROLS
WEATHER             Normal  Muddy  Frosty
CUSTOM LEAGUE       TOTAL TEAMS  HUMANS  POINTS FOR A WIN  PLAY EACH OTHER
KNOCKOUT            FIRST ROUND  QUARTER-FINAL  SEMI-FINAL  FINAL
ENDINGS             Top of the Ladder  DIY Champions
                    European Champions  League Drawn
```

`ISO CONTROL / NORMAL / ROTATED` is a CD-i peculiarity: the standard player
came with a thumbstick pad, but the format also shipped with a "roller
controller" and a trackball, and rotating the control axes by 45° was the
accepted fix for diagonal-first input devices.

`PASSWORD` and the `INVALID` / `ENTER` pair are the save system — the game
writes to `/nvr/csd`, the player's non-volatile RAM, but a password also lets
you carry a league across players.

Three control layouts are stored, one per line, with the button glyph as a
literal character in the string:

```
: = PASS    : = KICK    : = TACTI/PAUSE
; = PASS    ; = KICK    ; = TACTI/PAUSE
< = PASS    < = KICK    < = TACTI/PAUSE
```

`:`, `;` and `<` are `0x3A`–`0x3C`, three consecutive glyphs in the fonts —
button icons drawn into the character set where punctuation would be. The same
trick appears in `Start (.)    Cancel (..)` and `PRESS : OR ;`.

## The Tacti-Grid

The `abstract` file on the disc pitches it:

> Features the innovative Tacti-Grid (TM) to pick your team players and choose
> your custom tactics.

The screen behind it is `/eng_tscreen_gfx`, 512 × 240 with the picture in the
first 384 columns ([04-graphics.md](04-graphics.md)): three panels headed
`SQUAD`, `STATS` and `FORMATION`, with the formation itself an empty grid you
drop players onto, and a strip of set-piece assignments below it.

The strings that drive it:

```
Pre-Match   Half Time   Substitution
SQUAD  FORMATION  Player STATS  SUBSTITUTES
Penalty Taker   Defensive Free Kick   Attacking Free Kick
```

## Injuries and cards

```
YELLOW CARD :        RED CARD    :
: slightly hurt.     : in pain.
: injured.           : badly hurt.
```

The leading `:` is the substitution glyph again; each string is a suffix
appended to a player's name. Four injury grades, and a referee that can be
switched off entirely (`REFEREE` on the game-options menu).

## Commentary

Fourteen lines, and the option to turn them off:

```
Great goal              Unlucky!
Fantastic save          That's a penalty
What a malicious tackle!   That's a foul
A magnificent goal!     A fantastic strike
Great save              Bad foul
He puts it away         He won't be happy with that
He's hit the woodwork!  That was close!
```

These are *text*, not speech — there is no voice audio on the disc. The
executable refers to a file `/comment_gfx` to draw them on, and that file does
not exist ([11-leftovers.md](11-leftovers.md)).

## Two copyright notices, one of them real

The one that ships on screen, at `0x05690`:

```
       ALL RIGHTS OF THE PRODUCER
    AND OF THE OWNER OF THE WORK
           ARE RESERVED
      UNAUTHORISED COPYING,
 HIRING, RENTING, PUBLIC PERFORMANCE,
   TRANSMISSION AND/OR BROADCASTING
          ARE PROHIBITED.
```

and the one at `0x19F82`, sitting in the middle of the menu strings, between
`League Drawn` and the sound-test table:

```
La di da ... Put some copyright
Message crap in here or something
Written by Krisalis etc etc etc
```

Three lines of placeholder, laid out as three lines of a screen, still in the
retail binary.

## The credit roll

Rendered over `INTRO_GFX/credback`, a night shot of a floodlit stadium with
`CREDITS` down the right-hand side. Both the roll and the `biblio` file on the
disc name the same eight people:

| Role (in-game roll) | Role (`biblio`) | Name |
|---|---|---|
| Code | Pragrammed by | **Mark Adamson** |
| Arcade Engine | Arcade Engine Programmed by | **Pete Harrap** |
| Game Design | Game Design | **Neil Adamson**, **Ramo**, Mark Adamson |
| Arcade Graphics / Other Graphics | Artwork | **Neil Adamson**, **Phil Hackney**, Mark Adamson |
| Intro Animation | Intro Sequence | **Dave Colledge** |
| Sound Effects | Intro Music and Sound Effects | **John Avery** |
| Team Data Entry | — | Neil Adamson |

`biblio` says "Pragrammed by". It is a plain text file on a pressed disc, so
the typo is permanent.

The thanks list is more interesting than the credits:

```
Special thanks to...  ANDY MORTON  PAUL REID  TOM DRUMMOND  DARREN HEDGES
                      (At Philips)
                      PETE HARRAP  (Sorting it out!!)
                      (At Cross Products)  JASON BUTLER
                      (Thanks for the book sir)
                      DARRYL BLANDFORD  (Greetings Mate!)
                      RAMO
                      FRANS PENDERS  (Many thanks for the help!)
```

**Cross Products** of Leeds made the SNASM development systems — the 68000
cross-assembler and in-circuit debugger that British studios used for Mega
Drive, Saturn and 32X work. A CD-i title thanking Cross Products is a CD-i
title built on a Sega-era toolchain, which is consistent with everything else
in [11-leftovers.md](11-leftovers.md).
