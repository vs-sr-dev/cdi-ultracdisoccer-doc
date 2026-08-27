"""Render the CD-i bitmaps.

Every `*_gfx`, `*_sprts` and the pitch/background files are raw CLUT bitmaps:
one byte per pixel, no header, no compression, top-left first. The matching
`*_pal` file is a flat list of RGB triplets -- 64, 128 or 256 of them, which
is exactly one, two or four CD-i CLUT banks.

  python tools/cdigfx.py render FILE [-p PAL] [-w WIDTH] [-o OUT.png]
  python tools/cdigfx.py sheet OUTDIR         render everything it can
  python tools/cdigfx.py pal FILE             print a palette
"""
import sys, os, argparse
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_work', 'files')

# width, palette -- worked out from the file sizes and confirmed by eye
LAYOUT = {
    'nodv_gfx':                      (512, 'nodv_pal'),
    'intro_gfx.file':                (320, 'introb_pal'),
    'ip_gfx':                        (320, 'introb_pal'),
    'eng_introb_gfx':                (384, 'eng_introb_pal'),
    'eng_introf_gfx':                (320, 'introf_pal'),
    'eng_tscreen_gfx':               (512, 'PERM_GFX/eng_intro_pal'),
    'andrea_gfx':                    (384, 'andrea_pal'),
    'INTRO_GFX/credback':            (384, 'INTRO_GFX/credback_pal'),
    'INTRO_GFX/credback280':         (384, 'INTRO_GFX/credback280_pal'),
    'INTRO_GFX/krislogo':            (384, 'INTRO_GFX/krislogo_pal'),
    'INTRO_GFX/logo_gfx':            (384, 'INTRO_GFX/logo_pal'),
    'INTRO_GFX/philbump':            (384, 'INTRO_GFX/philbump_pal'),
    'PERM_GFX/loading_pic':          (128, 'PERM_GFX/loading_pic_pal'),
    'PERM_GFX/mypointa':             (16,  'PERM_GFX/mypointa_pal'),
    'PITCH_GFX/nmlpitch':            (512, 'PITCH_GFX/nmlpitch_pal'),
    'PITCH_GFX/drypitch':            (512, 'PITCH_GFX/drypitch_pal'),
    'PITCH_GFX/mudpitch':            (512, 'PITCH_GFX/mudpitch_pal'),
    'PITCH_GFX/icepitch':            (512, 'PITCH_GFX/icepitch_pal'),
    'PITCH_GFX/wetpitch':            (512, 'PITCH_GFX/wetpitch_pal'),
    'PITCH_GFX/refereer_gfx':        (48,  'PITCH_GFX/nmlpitch_pal'),
    'PITCH_GFX/refereey_gfx':        (48,  'PITCH_GFX/nmlpitch_pal'),
    'PITCH_GFX/tgoal':               (64,  'PITCH_GFX/pitchtop_pal'),
    'PITCH_GFX/bgoal':               (64,  'PITCH_GFX/pitchtop_pal'),
    'PITCH_GFX/t4wide_pitch':        (160, 'PITCH_GFX/tacti_pal'),
    'PITCH_GFX/t4font_sprts':        (128, 'PITCH_GFX/tacti_pal'),
    'PITCH_GFX/numbers':             (48,  'PITCH_GFX/pitch_pal'),
    'PITCH_GFX/lcd_sprts':           (64,  'PITCH_GFX/pitch_pal'),
    'PITCH_GFX/ball_sprts':          (16,  'PITCH_GFX/pitch_pal'),
    'PITCH_GFX/flags_sprts':         (16,  'PITCH_GFX/pitch_pal'),
    'PITCH_GFX/shadow_sprts':        (8,   'PITCH_GFX/pitch_pal'),
    'PLAYER_SPRTS/goalie_sprts':     (32,  'PITCH_GFX/nmlpitch_pal'),
    'SCOREBOARD_GFX/scorbord_gfx':   (384, 'SCOREBOARD_GFX/scorbord_pal'),
    'SAD_GFX/sadback_gfx':           (384, 'SAD_GFX/sad2_pal'),
    'SAD_GFX/sadomar1_gfx':          (256, 'SAD_GFX/sad_pal'),
    'SAD_GFX/sadomar2_gfx':          (256, 'SAD_GFX/sad_pal'),
    'CELEB_GFX/celeb_gfx':           (384, 'CELEB_GFX/celeb_pal'),
    'CELEB_GFX/cupeuro_gfx':         (160, 'CELEB_GFX/cups_pal'),
    'CELEB_GFX/cuplad_gfx':          (160, 'CELEB_GFX/cups_pal'),
    'CELEB_GFX/cuplge_gfx':          (160, 'CELEB_GFX/cups_pal'),
    'TOURN_GFX/ballback':            (384, 'TOURN_GFX/ballback_pal'),
    'TOURN_GFX/opt_baks':            (384, 'TOURN_GFX/opt_baks_pal'),
    'TOURN_GFX/eng_knockout_gfx':    (320, 'TOURN_GFX/knockout_pal'),
    'TSELECT_GFX/eng_tselect_gfx':   (384, 'TSELECT_GFX/tselect_pal'),
    'PERM_GFX/o16x16fnt_sprts':      (16,  'PERM_GFX/colours_pal'),
    'PERM_GFX/msfont_sprts':         (16,  'PERM_GFX/colours_pal'),
    'PERM_GFX/mtfont_sprts':         (16,  'PERM_GFX/colours_pal'),
    'PERM_GFX/propfont':             (16,  'PERM_GFX/colours_pal'),
    'INTRO_GFX/press2_gfx':          (32,  'TSELECT_GFX/tselect_pal'),
}
for i in list(range(1, 11)):
    LAYOUT[f'TOURN_GFX/kitg{i}_gfx'] = (64, 'TOURN_GFX/tmsplng_pal')
    LAYOUT[f'PLAYER_SPRTS/kit{i}_sprts'] = (32, 'PITCH_GFX/nmlpitch_pal')
LAYOUT['TOURN_GFX/kittick_gfx'] = (64, 'TOURN_GFX/tmsplng_pal')
# the abandoned localisation set: 320x224 for the five-screen group, 320x144
# for the knockout bracket. Every one of these files is entirely zeroes.
for lang in ('ger', 'fra', 'spa'):
    for base, w in (('introb_gfx', 320), ('introf_gfx', 320), ('knockout_gfx', 320),
                    ('tscreen_gfx', 320), ('tselect_gfx', 320)):
        LAYOUT[f'{lang}_{base}'] = (w, f'{lang}_intro_pal')


def load_pal(name):
    p = os.path.join(ROOT, name)
    b = open(p, 'rb').read()
    pal = [tuple(b[i:i + 3]) for i in range(0, len(b), 3)]
    return pal + [(255, 0, 255)] * (256 - len(pal))


def render(path, pal, width):
    b = open(path, 'rb').read()
    h = (len(b) + width - 1) // width
    b = b + b'\x00' * (width * h - len(b))
    im = Image.new('RGB', (width, h))
    im.putdata([pal[c] for c in b])
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd')
    ap.add_argument('arg', nargs='?')
    ap.add_argument('-p', '--pal')
    ap.add_argument('-w', '--width', type=int)
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    if a.cmd == 'pal':
        for i, c in enumerate(load_pal(a.arg)[:len(open(os.path.join(ROOT, a.arg), 'rb').read()) // 3]):
            print(f'{i:3d} #{c[0]:02x}{c[1]:02x}{c[2]:02x}')
    elif a.cmd == 'render':
        name = a.arg
        w, pal = LAYOUT.get(name, (a.width or 384, a.pal))
        w = a.width or w
        pal = a.pal or pal
        im = render(os.path.join(ROOT, name), load_pal(pal), w)
        out = a.out or (os.path.basename(name) + '.png')
        im.save(out)
        print(out, im.size)
    elif a.cmd == 'sheet':
        os.makedirs(a.arg, exist_ok=True)
        for name, (w, pal) in sorted(LAYOUT.items()):
            src = os.path.join(ROOT, name)
            if not os.path.exists(src):
                continue
            im = render(src, load_pal(pal), w)
            out = os.path.join(a.arg, name.replace('/', '_') + '.png')
            im.save(out)
            print(f'{name:<34} {im.size[0]}x{im.size[1]}')


if __name__ == '__main__':
    main()
