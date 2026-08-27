# Graphics inventory

Every bitmap and palette on the disc: size, the pixel-value range actually used,
and the geometry `tools/cdigfx.py` renders it at. "stride" marks files whose line
pitch is wider than the picture.

## Bitmaps

| file | bytes | values | distinct | geometry | notes |
|---|---:|---|---:|---|---|
| `PITCH_GFX/drypitch` | 393,216 | 0-121 | 122 | 512 x 768 |  |
| `PITCH_GFX/icepitch` | 393,216 | 0-125 | 122 | 512 x 768 |  |
| `PITCH_GFX/mudpitch` | 393,216 | 0-125 | 122 | 512 x 768 |  |
| `PITCH_GFX/nmlpitch` | 393,216 | 0-121 | 122 | 512 x 768 |  |
| `PITCH_GFX/wetpitch` | 393,216 | 0-120 | 119 | 512 x 768 |  |
| `TOURN_GFX/opt_baks` | 368,640 | 0-127 | 127 | 384 x 960 |  |
| `CELEB_GFX/celeb_gfx` | 245,760 | 0-31 | 21 | 384 x 640 |  |
| `eng_tscreen_gfx` | 122,880 | 0-128 | 90 | 512 x 240 | 384 px picture, 512-byte stride |
| `nodv_gfx` | 122,880 | 0-127 | 128 | 512 x 240 | 384 px picture, 512-byte stride |
| `INTRO_GFX/credback280` | 107,520 | 0-126 | 127 | 384 x 280 |  |
| `andrea_gfx` | 92,160 | 1-126 | 126 | 384 x 240 |  |
| `eng_introb_gfx` | 92,160 | 1-127 | 127 | 384 x 240 |  |
| `INTRO_GFX/credback` | 92,160 | 0-126 | 127 | 384 x 240 |  |
| `INTRO_GFX/krislogo` | 92,160 | 0-126 | 127 | 384 x 240 |  |
| `INTRO_GFX/logo_gfx` | 92,160 | 0-127 | 128 | 384 x 240 |  |
| `INTRO_GFX/philbump` | 92,160 | 0-127 | 125 | 384 x 240 |  |
| `PLAYER_SPRTS/goalie_sprts` | 92,160 | 3-255 | 48 | - | rlspr, 720 slots of 128 |
| `SAD_GFX/sadback_gfx` | 92,160 | 0-127 | 126 | 384 x 240 |  |
| `SCOREBOARD_GFX/scorbord_gfx` | 92,160 | 0-127 | 124 | 384 x 240 |  |
| `TOURN_GFX/ballback` | 92,160 | 64-127 | 60 | 384 x 240 |  |
| `TSELECT_GFX/eng_tselect_gfx` | 92,160 | 0-126 | 79 | 384 x 240 |  |
| `eng_introf_gfx` | 71,680 | 0-63 | 12 | 320 x 224 |  |
| `fra_introb_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `fra_introf_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `fra_tscreen_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `fra_tselect_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `ger_introb_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `ger_introf_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `ger_tscreen_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `ger_tselect_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `intro_gfx.file` | 71,680 | 0-47 | 12 | 320 x 224 |  |
| `ip_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `spa_introb_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `spa_introf_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `spa_tscreen_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `spa_tselect_gfx` | 71,680 | 0-0 | 1 | 320 x 224 | all zeroes |
| `SAD_GFX/sadomar1_gfx` | 57,344 | 0-31 | 16 | 256 x 224 |  |
| `SAD_GFX/sadomar2_gfx` | 57,344 | 0-31 | 16 | 256 x 224 |  |
| `PLAYER_SPRTS/kit10_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit1_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit2_sprts` | 53,248 | 3-255 | 45 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit3_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit4_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit5_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit6_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit7_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit8_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `PLAYER_SPRTS/kit9_sprts` | 53,248 | 2-255 | 49 | - | rlspr, 416 slots of 128 |
| `TOURN_GFX/eng_knockout_gfx` | 48,000 | 0-127 | 17 | 320 x 150 |  |
| `TSELECT_GFX/eng_tglass_gfx` | 46,754 | 0-31 | 31 | ? |  |
| `fra_knockout_gfx` | 46,080 | 0-0 | 1 | 320 x 144 | all zeroes |
| `ger_knockout_gfx` | 46,080 | 0-0 | 1 | 320 x 144 | all zeroes |
| `spa_knockout_gfx` | 46,080 | 0-0 | 1 | 320 x 144 | all zeroes |
| `PERM_GFX/o16x16fnt_sprts` | 46,080 | 0-63 | 17 | 16 x 2880 |  |
| `CELEB_GFX/cuplge_gfx` | 32,000 | 0-125 | 76 | 160 x 200 |  |
| `CELEB_GFX/cupeuro_gfx` | 25,600 | 0-125 | 65 | 160 x 160 |  |
| `CELEB_GFX/cuplad_gfx` | 25,600 | 0-119 | 82 | 160 x 160 |  |
| `PERM_GFX/propfont` | 23,296 | 0-8 | 4 | 16 x 1456 |  |
| `PITCH_GFX/t4font_sprts` | 16,640 | 0-63 | 18 | 128 x 130 |  |
| `PERM_GFX/msfont_sprts` | 8,896 | 1-14 | 3 | 16 x 556 |  |
| `PERM_GFX/mtfont_sprts` | 8,896 | 0-8 | 3 | 16 x 556 |  |
| `PERM_GFX/loading_pic` | 8,192 | 0-127 | 118 | 128 x 64 |  |
| `TOURN_GFX/kitg10_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg1_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg2_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg3_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg4_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg5_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg6_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg7_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg8_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kitg9_gfx` | 5,632 | 2-15 | 10 | 64 x 88 |  |
| `TOURN_GFX/kittick_gfx` | 5,632 | 0-13 | 3 | 64 x 88 |  |
| `PITCH_GFX/numbers` | 3,264 | 0-8 | 3 | 48 x 68 |  |
| `PITCH_GFX/refereer_gfx` | 2,304 | 64-126 | 40 | 48 x 48 |  |
| `PITCH_GFX/refereey_gfx` | 2,304 | 64-125 | 41 | 48 x 48 |  |
| `PITCH_GFX/lcd_sprts` | 2,176 | 0-8 | 4 | 64 x 34 |  |
| `PITCH_GFX/t4wide_pitch` | 2,080 | 0-112 | 9 | 160 x 13 |  |
| `PITCH_GFX/bgoal` | 2,048 | 0-76 | 14 | 64 x 32 |  |
| `PITCH_GFX/tgoal` | 2,048 | 0-73 | 11 | 64 x 32 |  |
| `INTRO_GFX/press2_gfx` | 1,696 | 0-255 | 34 | 32 x 53 |  |
| `PERM_GFX/mypointa` | 768 | 0-111 | 6 | 16 x 48 |  |
| `PITCH_GFX/flags_sprts` | 512 | 0-15 | 5 | 16 x 32 |  |
| `pointer_sprts` | 256 | 0-8 | 4 | ? |  |
| `PITCH_GFX/ball_sprts` | 256 | 0-8 | 4 | 16 x 16 |  |
| `PITCH_GFX/shadow_sprts` | 64 | 0-83 | 3 | 8 x 8 |  |

## Palettes

| file | bytes | entries | entry 0 |
|---|---:|---:|---|
| `CELEB_GFX/celeb_pal` | 192 | 64 | `#00FF00` |
| `CELEB_GFX/cups_pal` | 384 | 128 | `#00FF00` |
| `CELEB_GFX/philback_pal` | 384 | 128 | `#130B0F` |
| `INTRO_GFX/credback280_pal` | 768 | 256 | `#FFFFFF` |
| `INTRO_GFX/credback_pal` | 768 | 256 | `#FFFFFF` |
| `INTRO_GFX/krislogo_pal` | 768 | 256 | `#000000` |
| `INTRO_GFX/logo_pal` | 768 | 256 | `#00FF00` |
| `INTRO_GFX/philbump_pal` | 768 | 256 | `#000000` |
| `PERM_GFX/colours_pal` | 192 | 64 | `#000000` |
| `PERM_GFX/eng_intro_pal` | 768 | 256 | `#00FF00` |
| `PERM_GFX/loading_pic_pal` | 384 | 128 | `#00FF00` |
| `PERM_GFX/mypointa_pal` | 384 | 128 | `#FFFFFF` |
| `PITCH_GFX/drypitch_pal` | 384 | 128 | `#5B5B00` |
| `PITCH_GFX/icepitch_pal` | 384 | 128 | `#17630B` |
| `PITCH_GFX/mudpitch_pal` | 384 | 128 | `#575B0B` |
| `PITCH_GFX/nmlpitch_pal` | 384 | 128 | `#0B6B0B` |
| `PITCH_GFX/pitch_pal` | 192 | 64 | `#00FF00` |
| `PITCH_GFX/pitchtop_pal` | 384 | 128 | `#28B8BF` |
| `PITCH_GFX/tacti_pal` | 192 | 64 | `#00FF00` |
| `PITCH_GFX/tactiback_pal` | 384 | 128 | `#000000` |
| `PITCH_GFX/wetpitch_pal` | 384 | 128 | `#076B00` |
| `SAD_GFX/sad2_pal` | 384 | 128 | `#000000` |
| `SAD_GFX/sad_pal` | 192 | 64 | `#00FF00` |
| `SCOREBOARD_GFX/scorbord_pal` | 384 | 128 | `#0B0000` |
| `TOURN_GFX/ballback_pal` | 768 | 256 | `#00FF00` |
| `TOURN_GFX/knockout_pal` | 384 | 128 | `#000000` |
| `TOURN_GFX/opt_baks_pal` | 768 | 256 | `#0B0B0B` |
| `TOURN_GFX/options_pal` | 192 | 64 | `#00FF00` |
| `TOURN_GFX/tmsplng_pal` | 192 | 64 | `#00FF00` |
| `TSELECT_GFX/tglass_pal` | 384 | 128 | `#FFFFFF` |
| `TSELECT_GFX/tselect_pal` | 384 | 128 | `#000000` |
| `andrea_pal` | 768 | 256 | `#000000` |
| `eng_introb_pal` | 384 | 128 | `#FFFFFF` |
| `fra_intro_pal` | 192 | 64 | `#101010` |
| `ger_intro_pal` | 192 | 64 | `#101010` |
| `intro_pal` | 768 | 256 | `#00FF00` |
| `introb_pal` | 192 | 64 | `#00FF00` |
| `introf_pal` | 192 | 64 | `#00FF00` |
| `nodv_pal` | 768 | 256 | `#00FF00` |
| `spa_intro_pal` | 192 | 64 | `#101010` |
