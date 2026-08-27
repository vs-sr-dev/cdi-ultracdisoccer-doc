# 09 — The team database

From `0x1ABAC` to `0x2D8D7` — 77,100 bytes, a third of the executable — is one
flat array of team records. No index, no compression, no strings table: 75
records of 1,028 bytes, each with 21 player slots of 44 bytes.

## Record layout

```
team record, 1,028 bytes
  +0x000   2   zero
  +0x002  26   team name          "Borussia Monchengladbach"
  +0x01C  16   country            "Germany"
  +0x02C  12   short name         "Borussia.M"     fits the on-screen table
  +0x038   6   kit bytes
  +0x03E 924   21 player records
  +0x3DA  42   zero

player record, 44 bytes
  +0x00   26   name               "Karl Heinz Viedle"
  +0x1A    1   flags
  +0x1B    1   per-player id, 0..147
  +0x1C    9   ratings, 0..100
  +0x25    2   always 100, 100
  +0x27    5   zero
```

Names are NUL-terminated and NUL-padded, not length-prefixed. The 42 spare
bytes at the end of a team record are two bytes short of a 22nd player slot,
which is a slightly uncomfortable place for a structure to land and suggests
the squad size was 21 from early on.

## The 75 records

```
   0 – 21   England       Arsenal … Wimbledon                 (22 clubs)
  22 – 29   Germany       Bayer 04 Leverkusen … SV Werder Bremen
  30 – 37   Spain         Athletic Bilbao … Valencia CF
  38 – 45   France        AJ Auxerre … AS Saint-Etienne
  46 – 65   Europe        Ajax, Anderlecht, AEK Athens, Austria Salzburg,
                          Benfica, Slovan Bratislava, Steau Bucharest,
                          Galatasaray, Servette Geneva, IFK Gothenburg,
                          Maccabi Haifa, Dinamo Kiev, AC Milan,
                          Spartak Moscow, Sparta Prague, Rangers,
                          Silkeborg, Hadjuk Split, VAC FC Samsung,
                          Legia Warsaw                        (20 clubs)
  66 – 69   select XIs    English / French / German / Spanish League Stars
  70        Europe        Euro-League Stars
  71        World         All-Time Greats
  72        England       Rotherham United
  73        England       Krisalis
  74        FUG land      Ken Dodds dads dogs dead
```

1,454 players in 1,575 slots. The last three records are not football teams;
see [11-leftovers.md](11-leftovers.md).

Record 75 at `0x2D8D8` is present but blank, and the array stops there.

## The names are deliberately wrong

Every top-flight player on this disc is misspelled, and misspelled
*consistently* — a letter changed, never a name invented:

```
Ian Write        David Sceaman     Nigel Wintaburn   Tony Adamson
Alan Sheron      Graeme Le-Sawx    Glenn Hodd        David Rocustle
Gareth Northgate Daniel Amokocha   Tony Cotty        Dion Dublin
Paul McGrach     Dwight Vorke      Ugo Eiogi         Matthias BritKrutz
Lothar Matthaus  Oliver Khan       Mehmet Schull     Gorginho
```

This is the standard 1990s answer to not holding a PFA licence, and it is
applied to all 65 real clubs.

It is not applied to **Rotherham United**, whose 21 players are spelled
correctly — Lee Glover, Shaun Goater, Ian Breckin, Chris Wilder, Paul Hurst,
Steve Cherry, John McGlashan — nor to the joke team at record 74, which lists
Roberto Baggio, Romario, Franco Baresi, Dennis Bergkamp, Gabriel Batistuta,
Gianfranco Zola, Alen Boksic, Faustino Asprilla and Gianluigi Lentini under
their real names.

Krisalis were based in Rotherham. The one squad in the game they got right is
their local club, in the third tier, with no licence problem worth worrying
about.

## The ratings

Nine bytes, each 0–100, followed by two bytes that are 100, 100 in all 1,454
players. `Krisalis` (record 73) is the clearest read on what they mean, because
it is a staff team ordered from best to worst:

```
Ramo             80 59 57 78 68 63 36 59 61
Mark Adamson     76 71 46 50 63 85 26 49 48
Neil Adamson     89 93 47 54 56 48 64 53 78
...
Pete Harrap      21 29 14 15 15  3  3  1  4
Siobhan Moron    23 22  8  8  7  7  6  6 10
DeeDee           37  7  0  5  0  0  0  0  0
```

Nine attributes falling off a cliff down the list. Which is which is
[open](12-open-questions.md) — nothing in the strings names them, and the
`Player STATS` screen is drawn with the Tacti-Grid font rather than with
labels.

`All-Time Greats` is the useful control group: Pelé, Maradona, Cruyff and
Puskás sit at 89–100 across the board, Facchetti and Di Stéfano in the low 90s.
Somebody sat down and rated twenty-one legends by hand.

## The flags byte

```
0x80  828      0xa0   66
0x81   41      0xa1   10
0x82  387      0xa2   64
0x83   23      0xa3   14
0x03   15      0x23    6
```

Bit 7 is set on 1,433 of 1,454 players and clear on the whole of record 74, the
joke team — which was almost certainly typed in by hand into a tool that did
not set it.

Bit 5 is set on 154 players, and which players is not random. In `All-Time
Greats` it is set on Pelé, Garrincha, Eusébio, Tostão and Carlos Alberto and
clear on Beckenbauer, Moore, Puskás, Banks, Cruyff and Charlton. In Arsenal it
is set on Ian Wright, Kevin Campbell and Paul Davis; in Aston Villa on John
Fashanu, Earl Barrett, Dalian Atkinson, Dwight Yorke, Paul McGrath and Ugo
Ehiogu. It selects a darker sprite. The correlation is not perfect — Everton's
Daniel Amokachi has the bit clear — which is what a hand-entered flag across
1,454 rows looks like.

Bit 1 is set on 488 players and bit 0 on 88, and neither has a reading yet.

## The kit bytes

Six bytes at `+0x038`. Across the 75 records:

```
nibble  0   always 1
nibble  1   1..6
nibbles 2-3 mostly 9
nibbles 4-11  0,1,2,5,7,8,9,11,12,13,14
```

The bottom eight nibbles look like colour indices: the ten `TOURN_GFX/kitg*`
swatch files use pixel values 2–15, ten distinct, and eight nibbles is a
sensible way to describe a shirt, shorts, socks and trim in home and away. The
top four are not colours. This is a reading, not a result;
[open](12-open-questions.md).

## The blurb that was never written

`Player STATS` has a companion: a team description. Exactly one is written.

```
0x1A1DC   MANCHESTER UNITED
          won the first two Premier
          League championships.
          They are now the dominant
          force in the English
          game, playing stylish,
          entertaining football, which
          is a delight to watch.
```

Seven lines, NUL-separated, for record 12 of 75. There is no second blurb
anywhere in the module. Whatever screen was going to show a paragraph about
your club got one team's worth of copy and then the feature stopped.

## Reproducing

```
python tools/cditeams.py list          75 records, one line each
python tools/cditeams.py squad NAME    one squad with flags, ids and ratings
python tools/cditeams.py dump          markdown, everything
```

The full dump is in [notes/team-database.md](../notes/team-database.md).
