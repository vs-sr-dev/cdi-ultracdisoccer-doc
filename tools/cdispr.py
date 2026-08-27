"""Decode the `*_sprts` sprite banks.

A bank is a flat array of fixed-size slots. Inside a slot the sprite is
run-length coded, one line at a time:

    0x00..0x7F   one pixel of that CLUT index
    0x80..0xFD   skip (n & 0x7F) transparent pixels
    0xFF         end of line
    0xFE         filler -- pads the slot out to its fixed size

The executable calls the format `rlspr` (there is a dangling reference to a
file `/kit1_rlspr` that the disc does not carry).

  python tools/cdispr.py info FILE
  python tools/cdispr.py sheet FILE OUT.png [-p PAL] [-s SLOT]
"""
import sys, os, argparse
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_work', 'files')
SLOT = {'goalie_sprts': 128, 'kit1_sprts': 128, 'kit2_sprts': 128, 'kit3_sprts': 128,
        'kit4_sprts': 128, 'kit5_sprts': 128, 'kit6_sprts': 128, 'kit7_sprts': 128,
        'kit8_sprts': 128, 'kit9_sprts': 128, 'kit10_sprts': 128}


def decode(slot):
    """One slot -> list of rows, each row a list of ints (-1 = transparent)."""
    rows, cur, i = [], [], 0
    while i < len(slot):
        v = slot[i]
        i += 1
        if v == 0xFF:
            rows.append(cur)
            cur = []
        elif v == 0xFE:
            break
        elif v & 0x80:
            cur += [-1] * (v & 0x7F)
        else:
            cur.append(v)
    if cur:
        rows.append(cur)
    while rows and not rows[-1]:
        rows.pop()
    return rows


def frames(path, slotsize):
    b = open(path, 'rb').read()
    return [decode(b[o:o + slotsize]) for o in range(0, len(b), slotsize)]


def load_pal(name):
    b = open(os.path.join(ROOT, name), 'rb').read()
    p = [tuple(b[i:i + 3]) for i in range(0, len(b), 3)]
    return p + [(255, 0, 255)] * (256 - len(p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('file'); ap.add_argument('out', nargs='?')
    ap.add_argument('-p', '--pal', default='PITCH_GFX/nmlpitch_pal')
    ap.add_argument('-s', '--slot', type=int, default=128)
    ap.add_argument('-c', '--cols', type=int, default=32)
    a = ap.parse_args()
    path = a.file if os.path.exists(a.file) else os.path.join(ROOT, a.file)
    fr = frames(path, a.slot)
    if a.cmd == 'info':
        used = [max((len(r) for r in f), default=0) for f in fr]
        hgt = [len(f) for f in fr]
        print(f'{len(fr)} slots of {a.slot} bytes')
        print(f'widths  {min(used)}..{max(used)}   heights {min(hgt)}..{max(hgt)}')
        empty = sum(1 for f in fr if not f)
        print(f'empty slots: {empty}')
        return
    W = max(max((len(r) for r in f), default=0) for f in fr) + 2
    H = max(len(f) for f in fr) + 2
    pal = load_pal(a.pal)
    cols = a.cols
    rowsn = (len(fr) + cols - 1) // cols
    im = Image.new('RGB', (cols * W, rowsn * H), (255, 0, 255))
    px = im.load()
    for n, f in enumerate(fr):
        ox, oy = (n % cols) * W, (n // cols) * H
        for y, row in enumerate(f):
            for x, c in enumerate(row):
                if c >= 0:
                    px[ox + x, oy + y] = pal[c]
    im.save(a.out)
    print(a.out, im.size, len(fr), 'frames')


if __name__ == '__main__':
    main()
