"""RTF/intro_anim -- the CD-i Digital Video intro.

A real-time file is not a plain byte stream: it is a run of Mode 2 Form 2
sectors whose subheaders carry the channel and the real-time flags. Reading it
through the directory record (2048 bytes per sector, Form 1) yields garbage.

Here every sector is 2324 bytes and the payload is an MPEG-1 system stream --
the same one a CD-i player feeds to the Digital Video cartridge. Sectors tagged
neither VIDEO nor AUDIO are bitrate padding and carry nothing.

  python tools/cdirtf.py map                sector census
  python tools/cdirtf.py demux OUT.mpg      MPEG-1 system stream
  python tools/cdirtf.py info               sequence / audio headers
"""
import sys, os, struct, collections, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdilib

START, COUNT = 3203, 1992          # /RTF/intro_anim, from the directory record

ASPECT = {1: '1.0000 (square)', 2: '0.6735', 3: '0.7031 (16:9)', 4: '0.7615',
          5: '0.8055', 6: '0.8437', 7: '0.8935', 8: '0.9157', 9: '0.9815',
          10: '1.0255', 11: '1.0695', 12: '1.0950', 13: '1.1575', 14: '1.2015'}
FPS = {1: 23.976, 2: 24, 3: 25, 4: 29.97, 5: 30, 6: 50, 7: 59.94, 8: 60}
MP2_RATE = [None, 44100, 48000, 32000]
MP2_BITRATE = [None, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384]


def sectors(disc):
    for lba in range(START, START + COUNT):
        s = disc.raw(lba)
        yield lba, s[16], s[17], s[18], s[19], s[24:24 + 2324]


def demux(disc):
    out = bytearray()
    for lba, f, ch, sm, co, payload in sectors(disc):
        if sm & (cdilib.SM_VIDEO | cdilib.SM_AUDIO):
            out += payload
    return bytes(out)


def cmd_map(disc):
    c = collections.Counter()
    for lba, f, ch, sm, co, _ in sectors(disc):
        c[(f, ch, sm, co)] += 1
    print(f'{"file":>4} {"chan":>4} {"submode":>7}  {"flags":<24}{"coding":>7} {"sectors":>8}')
    for (f, ch, sm, co), n in sorted(c.items()):
        print(f'{f:>4} {ch:>4}    0x{sm:02x}  {cdilib.submode_str(sm):<24}   0x{co:02x} {n:>8}')
    tot = sum(c.values())
    pad = sum(n for (f, ch, sm, co), n in c.items()
              if not sm & (cdilib.SM_VIDEO | cdilib.SM_AUDIO))
    print(f'\n{tot} sectors, {pad} of them bitrate padding '
          f'({pad * 100 / tot:.1f}%), {tot * 2324:,} bytes raw')


def cmd_info(disc):
    b = demux(disc)
    print(f'demuxed {len(b):,} bytes')
    i = b.find(b'\x00\x00\x01\xb3')
    if i >= 0:
        h = b[i + 4:i + 12]
        w = (h[0] << 4) | (h[1] >> 4)
        ht = ((h[1] & 0x0F) << 8) | h[2]
        ar, fr = h[3] >> 4, h[3] & 0x0F
        br = ((h[4] << 10) | (h[5] << 2) | (h[6] >> 6)) & 0x3FFFF
        print(f'sequence header @0x{i:x}: {w}x{ht}  {FPS.get(fr, fr)} fps  '
              f'aspect {ASPECT.get(ar, ar)}  {br * 400:,} bit/s')
    j = b.find(b'\x00\x00\x01\xc0')
    print(f'audio PES 0x{0xc0:02x} first at 0x{j:x}' if j >= 0 else 'no audio PES 0xC0')
    k = 0
    while True:
        k = b.find(b'\xff\xfd', k + 1)
        if k < 0 or k > len(b) - 4:
            break
        h = b[k:k + 4]
        layer = (h[1] >> 1) & 3
        bri = h[2] >> 4
        sri = (h[2] >> 2) & 3
        mode = h[3] >> 6
        if layer == 2 and sri < 3 and 0 < bri < 15 and MP2_RATE[sri]:
            print(f'MPEG audio @0x{k:x}: layer II  {MP2_RATE[sri]} Hz  '
                  f'{MP2_BITRATE[bri]} kbit/s  mode {["stereo","joint","dual","mono"][mode]}')
            break
    n = b.count(b'\x00\x00\x01\x00')
    print(f'{n} picture start codes')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('out', nargs='?')
    a = ap.parse_args()
    d = cdilib.Disc()
    if a.cmd == 'map':
        cmd_map(d)
    elif a.cmd == 'info':
        cmd_info(d)
    elif a.cmd == 'demux':
        open(a.out, 'wb').write(demux(d))
        print(a.out, os.path.getsize(a.out), 'bytes')
