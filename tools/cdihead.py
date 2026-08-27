"""The 2,269 sectors that sit in front of the file system.

They are well-formed Mode 2 Form 2 sectors -- correct sync, correct MSF
header, correct EDC -- but their user data is not plain. XOR it with the
ECMA-130 Annex B scrambler sequence and 1,064 of them become all zeroes while
1,203 become smooth 16-bit stereo PCM whose two channels are identical.

  python tools/cdihead.py map           classify every sector
  python tools/cdihead.py wav OUTDIR    write the descrambled audio out
  python tools/cdihead.py check         verify sync, header and EDC
"""
import sys, os, struct, wave, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdilib

HEAD_END = 2269          # first sector of the file system (the path table)
SYNC = b'\x00' + b'\xff' * 10 + b'\x00'


def scrambler():
    """ECMA-130 Annex B: 15-bit LFSR, x^15 + x + 1, preset $0001, LSB first."""
    reg, out = 0x0001, bytearray()
    for _ in range(2340):
        b = 0
        for bit in range(8):
            b |= (reg & 1) << bit
            fb = (reg ^ (reg >> 1)) & 1
            reg = (reg >> 1) | (fb << 14)
        out.append(b)
    return bytes(out)


TABLE = scrambler()
KEY = TABLE[12:12 + 2324]          # the part that lines up with Form 2 user data


def edc(data):
    tbl = []
    for i in range(256):
        c = i
        for _ in range(8):
            c = (c >> 1) ^ (0xD8018001 if c & 1 else 0)
        tbl.append(c)
    r = 0
    for b in data:
        r = (r >> 8) ^ tbl[(r ^ b) & 0xFF]
    return r


def descramble(disc, lba):
    return bytes(a ^ b for a, b in zip(disc.raw(lba)[24:24 + 2324], KEY))


def classify(disc):
    runs, cur = [], None
    for lba in range(HEAD_END):
        s = disc.raw(lba)
        sm = s[cdilib.HDR + 2]
        if not sm & cdilib.SM_FORM2:
            kind = 'volume descriptor'
        else:
            kind = 'scrambled zeroes' if set(descramble(disc, lba)) == {0} else 'scrambled PCM'
        if cur and cur[0] == kind and cur[2] == lba - 1:
            cur[2] = lba
        else:
            if cur:
                runs.append(cur)
            cur = [kind, lba, lba]
    runs.append(cur)
    return runs


def cmd_map(disc):
    for kind, a, b in classify(disc):
        n = b - a + 1
        print(f'{a:5d}-{b:<5d} {n:5d} sectors  {n * 2324:>9,} B  {kind}')


def cmd_check(disc):
    bad_sync = bad_hdr = bad_edc = 0
    for lba in range(HEAD_END):
        s = disc.raw(lba)
        if s[:12] != SYNC:
            bad_sync += 1
        m, sec, fr = lba + 150, 0, 0
        mm, rem = divmod(m, 75 * 60)
        ss, ff = divmod(rem, 75)
        want = bytes([int(f'{v:02d}', 16) for v in (mm, ss, ff)]) + bytes([s[15]])
        if s[12:16] != want:
            bad_hdr += 1
        if s[cdilib.HDR + 2] & cdilib.SM_FORM2:
            stored = struct.unpack('<I', s[2348:2352])[0]
            if stored != edc(s[16:2348]):
                bad_edc += 1
    print(f'{HEAD_END} sectors: {bad_sync} bad sync, {bad_hdr} bad header, {bad_edc} bad EDC')


def cmd_wav(disc, outdir):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for kind, a, b in classify(disc):
        if kind != 'scrambled PCM':
            continue
        n += 1
        buf = bytearray()
        for lba in range(a, b + 1):
            buf += descramble(disc, lba)[:2304]
        path = os.path.join(outdir, f'head_{n}_{a}-{b}.wav')
        with wave.open(path, 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(44100)
            w.writeframes(bytes(buf))
        print(f'{path}  {len(buf) // 4} frames  {len(buf) / 4 / 44100:.2f} s')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('out', nargs='?')
    a = ap.parse_args()
    d = cdilib.Disc()
    {'map': lambda: cmd_map(d), 'check': lambda: cmd_check(d),
     'wav': lambda: cmd_wav(d, a.out or '_work/headwav')}[a.cmd]()
