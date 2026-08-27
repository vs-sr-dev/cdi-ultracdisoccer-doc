# String inventory

Everything legible in `/CMDS/cdi_demo`, grouped by what it is. Offsets are
file offsets, which for module 1 are also offsets from the module header.
Reproduce with `tools/cdistrings.py`.

## Loader and error text (0x02BE8 – 0x02F12)

```
YOUR DISK MAY BE DIRTY OR DAMAGED.  WE RECOMMEND THAT YOU REMOVE THE DISK
AND CLEAN IT.  TO TRY AGAIN REPLACE THE DISK AND RESET THE CDI PLAYER.
IF THE PROBLEM PERSISTS CONSULT YOUR CDI SUPPLIER.

   A PROBLEM OCCURRED WHILE LOADING..
        .. COULD NOT OPEN FILE
      .. FAILED DURING FILE READ
        .. MEMORY ALLOC ERROR
      .. COULD NOT CLOSE A FILE
      .. COULD NOT GET FILE SIZE
   YOUR DISK MAY BE DIRTY OR DAMAGED
 WE RECOMMEND THAT YOU REMOVE THE DISK
  AND CLEAN IT. THEN RESTART THE GAME
Error Freeing Memory!
```

The first block is one long run with the line breaks baked in as runs of
spaces; the second is a table of centred 37-column lines, which is what the
8x8 font renders across a 384-pixel screen.

## Digital Video cartridge (0x05B0E)

```
          YOU DO NOT HAVE YOUR
      DIGITAL VIDEO CARTRIDGE LOADED
       PLEASE SWITCH OFF YOUR CDI PLAYER
       INSERT THE CARTRIDGE AND RESTART.
        IF YOU DO NOT HAVE A CARTRIDGE
             PLEASE CONTACT YOUR
      LOCAL CDI SUPPLIER FOR DETAILS.
```

## Rights notice (0x05690)

```
       ALL RIGHTS OF THE PRODUCER
    AND OF THE OWNER OF THE WORK
           ARE RESERVED
      UNAUTHORISED COPYING,
 HIRING, RENTING, PUBLIC PERFORMANCE,
   TRANSMISSION AND/OR BROADCASTING
          ARE PROHIBITED.
```

## Credit roll (0x06E57 – 0x076AF)

```
Game Developed by       KRISALIS SOFTWARE
                        PHILIPS
                        INTERACTIVE MEDIA
Code                    MARK ADAMSON
Arcade Engine           PETE HARRAP
Arcade Graphics         NEIL ADAMSON
                        PHIL HACKNEY
Intro Animation         DAVE COLLEDGE
Other Graphics          NEIL ADAMSON
                        MARK ADAMSON
Sound Effects           JOHN AVERY
Game Design             NEIL ADAMSON
Team Data Entry         NEIL ADAMSON
Special thanks to...    ANDY MORTON
                        PAUL REID
                        TOM DRUMMOND
                        DARREN HEDGES
                        (At Philips)
                        PETE HARRAP
                        (Sorting it out!!)
                        (At Cross Products)
                        JASON BUTLER
                        (Thanks for the book sir)
                        DARRYL BLANDFORD
                        (Greetings Mate!)
                        RAMO
                        FRANS PENDERS
                        (Many thanks for the help!)
```

## Match flow (0x0944E – 0x095E8)

```
Half Time (EXTRA TIME)   PENALTY SHOOT OUT   FULL TIME   HALF TIME
```

## Menus and screens (0x19B46 – 0x19F62)

```
Pre-Match  Half Time  Substitution
SQUAD  FORMATION  Player STATS  SUBSTITUTES
Penalty Taker  Defensive Free Kick  Attacking Free Kick
YELLOW CARD :   RED CARD    :
: slightly hurt.  : in pain.  : injured.  : badly hurt.
Match Result  Penalties  Press 2
Select Kit  LEFT = KIT 1  RIGHT= KIT 2  2 = Done.
Week number
Instant Action  Head To Head  League Ladder  Custom League
Champions Cup   Champions League
COMPETITION  OPTIONS  PASSWORD  MATCH LENGTH  ISO CONTROL
4 MINUTES  7 MINUTES  10 MINUTES   NORMAL  ROTATED
REDEFINE KEYS  TEST TUNE  TEST SFX  CANCEL
TOTAL TEAMS  HUMANS  POINTS FOR A WIN  PLAY EACH OTHER  START
Final Standings  ENTER  INVALID
FIRST ROUND  QUARTER-FINAL  SEMI-FINAL  FINAL
SOUND  GAME OPTIONS  CONTROLS  MUSIC  WEATHER  COMMENTARY  REFEREE
: = PASS   : = KICK   : = TACTI/PAUSE     (three control layouts)
Normal  Muddy  Frosty
Top of the Ladder  DIY Champions  European Champions  League Drawn
```

## Placeholder copyright, never replaced (0x19F82)

```
La di da ... Put some copyright
Message crap in here or something
Written by Krisalis etc etc etc
```

## Sound test table (0x19FE4 – 0x1A0B7)

```
BLANK (MUSICOFF)  TITLE THEME  WIN EUROPEAN CUP  WIN CUSTOM  WIN LEAGUE
CREDITS  LOSE LEAGUE  LOSE CUP  INGAME CROWD
CROWD FX 1  CROWD FX 2  CROWD FX 3  CROWD FX 4
CHEER 1  KICK 1  PLAYER FOULED  CROSSBAR  SHORT REF  LONG REF
VALID  INVALID
```

## Commentary (0x1A0C5 – 0x1A19E)

```
Great goal            Unlucky!               Fantastic save
That's a penalty      What a malicious tackle!   That's a foul
A magnificent goal!   A fantastic strike     Great save
Bad foul              He puts it away        He won't be happy with that
He's hit the woodwork!   That was close!
```

## Debug (0x1A1C3, 0x2E64B, 0x2EA9D, 0x3383C, 0x33D2C)

```
Fuckin' strings fucked
QUIT   GAME WINDOW
TV   MONITOR
CHEAT MODE ON
PRESS : OR ;
Start (.)    Cancel (..)
```

## Team blurb (0x1A1DC) — the only one written

```
MANCHESTER UNITED
won the first two Premier
League championships.
They are now the dominant
force in the English
game, playing stylish,
entertaining football, which
is a delight to watch.
```

## Devices and modules

```
/nvr/csd        (0x34C94, 0x3733C)  the player's non-volatile RAM
/RTF/intro_anim (0x35898)           opened by absolute path
line_event      (0x2D99A)           OS-9 event name
cdi_syst        (0x2D9A8)           the trap module linked into the file
cdi_main.mod    (0x348A8)           module 1's own name
```
