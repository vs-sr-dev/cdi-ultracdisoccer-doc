"""The team and player database inside /CMDS/cdi_demo.

The table starts at 0x1ABAC and holds fixed 1,028-byte records:

    +0x000  2   zero
    +0x002  26  team name
    +0x01C  16  country
    +0x02C  12  short name (fits the on-screen table)
    +0x038  6   kit bytes -- see notes/team-database.md
    +0x03E  21 x 44-byte player records
    +0x3DA  42  spare (just short of a 22nd player slot)

and a player record is:

    +0x00   26  name
    +0x1A   1   flags
    +0x1B   1   unidentified per-player id
    +0x1C   9   ratings, 0..100
    +0x25   2   always 100, 100
    +0x27   5   zero

  python tools/cditeams.py list
  python tools/cditeams.py squad TEAM
  python tools/cditeams.py dump          markdown, every team and player
"""
import sys, os, argparse

BASE, STRIDE, NPLAYER, PSTRIDE = 0x1ABAC, 0x404, 21, 0x2C
EXE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', '_work', 'files', 'CMDS', 'cdi_demo')


def cstr(b, off, n):
    return b[off:off + n].split(b'\x00')[0].decode('latin-1').rstrip()


def teams(path=None):
    b = open(path or EXE, 'rb').read()
    out = []
    i = 0
    while True:
        o = BASE + i * STRIDE
        if o + STRIDE > len(b):
            break
        name = cstr(b, o + 2, 26)
        if not name:
            break
        t = dict(index=i, offset=o, name=name,
                 country=cstr(b, o + 0x1C, 16), short=cstr(b, o + 0x2C, 12),
                 kit=b[o + 0x38:o + 0x3E], players=[])
        for p in range(NPLAYER):
            po = o + 0x3E + p * PSTRIDE
            pn = cstr(b, po, 26)
            if not pn:
                continue
            t['players'].append(dict(
                name=pn, flags=b[po + 0x1A], id=b[po + 0x1B],
                ratings=list(b[po + 0x1C:po + 0x25]),
                tail=list(b[po + 0x25:po + 0x27])))
        out.append(t)
        i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('arg', nargs='?')
    a = ap.parse_args()
    ts = teams()
    if a.cmd == 'list':
        print(f'{"#":>3} {"offset":>8}  {"team":<26}{"country":<16}{"short":<12}{"kit":<14}players')
        for t in ts:
            print(f'{t["index"]:>3} 0x{t["offset"]:06x}  {t["name"]:<26}{t["country"]:<16}'
                  f'{t["short"]:<12}{t["kit"].hex(" "):<18}{len(t["players"])}')
        print(f'\n{len(ts)} records, {sum(len(t["players"]) for t in ts)} players')
    elif a.cmd == 'squad':
        for t in ts:
            if a.arg.lower() in t['name'].lower():
                print(f'{t["name"]}  ({t["country"]})   kit {t["kit"].hex(" ")}')
                for p in t['players']:
                    print(f'  {p["name"]:<24} flags 0x{p["flags"]:02x}  id {p["id"]:3d}  '
                          + ' '.join(f'{v:3d}' for v in p['ratings']))
    elif a.cmd == 'dump':
        for t in ts:
            print(f'\n### {t["index"]}. {t["name"]} — {t["country"]}\n')
            print(f'short name `{t["short"]}`, kit bytes `{t["kit"].hex(" ")}`, '
                  f'record at `0x{t["offset"]:06x}`\n')
            print('| player | flags | id | ratings |')
            print('|---|---|---|---|')
            for p in t['players']:
                print(f'| {p["name"]} | 0x{p["flags"]:02x} | {p["id"]} | '
                      + ' '.join(str(v) for v in p['ratings']) + ' |')


if __name__ == '__main__':
    main()
