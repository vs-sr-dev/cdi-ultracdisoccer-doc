# 06 — Fonts

Five fonts ship on this disc, in three different storage layouts, plus a sixth
linked into the executable. Nobody unified them.

| File | Bytes | Cell | Layout | Glyphs |
|---|---:|---|---|---:|
| in `cdi_demo` at `0x0050` | 232 | 8 × 8, 1 bit | packed rows | 29 |
| `PERM_GFX/msfont_sprts` | 8,896 | 8 × 8, 8 bit | glyph-major | 139 |
| `PERM_GFX/mtfont_sprts` | 8,896 | 8 × 8, 8 bit | glyph-major | 139 |
| `PERM_GFX/o16x16fnt_sprts` | 46,080 | 16 × 16, 8 bit | 16-line strip | 180 |
| `PERM_GFX/propfont` | 23,296 | 16 tall, 8 bit | 16-line strip | proportional |
| `PITCH_GFX/t4font_sprts` | 16,640 | ? | ? | ? |

## Glyph-major: `msfont_sprts` and `mtfont_sprts`

Each glyph is a contiguous 64-byte block, eight rows of eight bytes. 139
glyphs, starting at space.

Read them out and the character set is unmistakable. Every glyph carries a
one-pixel drop shadow in a second colour index, so the shapes look heavier than
they are:

```
  ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
@ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ `
a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
```

Plain ASCII `0x20`–`0x7E` runs straight through, and then the block that
follows is the giveaway. Spelled out properly it reads

```
Ç ü é â ä à å ç ê ë è ï î ì Ä Å É æ Æ ô ö ò û ù ÿ Ö Ü ¢ £ ¥ ₧ ƒ
á í ó ú ñ Ñ ª º ¿
```

which is **IBM PC code page 437**, positions `0x80` to `0xA8`, in order,
including the peseta sign and the florin. A Philips CD-i game running OS-9 on a
68000 carries a DOS code page because the artist drew the font on a PC and the
tool that converted it walked the PC character set.

139 glyphs is exactly CP437 `0x20` through `0xAA`. Nothing on this disc prints
an accented character — the only languages that shipped are English menus and
English commentary — so the whole upper half is dead weight, resident in memory
for the length of the game.

`ms` and `mt` are the same alphabet in different colours: `msfont` uses indices
1–14, `mtfont` uses 0–8, three distinct values each. Two colourways of one
font, 8,896 bytes apiece, both permanently resident.

## Strip layout: `o16x16fnt_sprts` and `propfont`

These two are stored as a **single image 16 pixels tall and as wide as it
needs to be** — 2,880 and 1,456 pixels respectively. Glyph *n* is a vertical
slice of that strip, not a contiguous block, so reading them as 256-byte cells
produces recognisable letters sheared across cell boundaries, which is a
convincing enough near-miss to waste an afternoon on.

`o16x16fnt_sprts` is a fixed 16 × 16 set: 180 glyphs, digits through
lower-case. `propfont` is proportional — a serif italic face, upper and lower
case, punctuation, digits — and the strip carries no width table. The widths
must be in the executable; where, is [open](12-open-questions.md).

## Digits: `PITCH_GFX/numbers`

3,264 bytes of 8 × 8 cells, glyph-major, 51 of them: the digits in several
colourways with a drop shadow baked in.

```
. . 1 1 1 . . .
. . 1 8 1 8 . .
. . 1 8 1 8 . .
. . 1 8 1 8 . .
. . 1 1 1 8 . .
. . . 8 8 8 . .
```

Index 1 is the face, index 8 is the shadow. `PITCH_GFX/lcd_sprts` is the same
idea at 2,176 bytes — 34 cells of 8 × 8, the scoreboard's LCD digits.

## The one that did not come out

`PITCH_GFX/t4font_sprts` — the Tacti-Grid font — is 16,640 bytes with pixel
values 0–63 and eighteen distinct values. It is not glyph-major at 8 × 8, not a
16-line strip, and not `rlspr` (no byte in it exceeds `0x3F`). Its factors
allow 8 × 2080, 10 × 1664, 13 × 1280, 16 × 1040, 20 × 832, 26 × 640, 32 × 520,
65 × 256 and 128 × 130; none of them renders. It probably has a header. It is
[open](12-open-questions.md).

## Reproducing

`tools/cdigfx.py sheet` renders the strip and glyph-major fonts with the
layouts above; the raw strips are easiest to read at their natural height:

```
python tools/cdigfx.py render PERM_GFX/propfont -w 1456 -p PERM_GFX/colours_pal
python tools/cdigfx.py render PERM_GFX/o16x16fnt_sprts -w 2880 -p PERM_GFX/colours_pal
```
