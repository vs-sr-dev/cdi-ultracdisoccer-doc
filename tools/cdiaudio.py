"""The SAMPLES/*_sfx effects, and the CD-i ADPCM decoder.

Each effect is an AIFF-C `FORM`/`AIFF` file whose sample data sits in a
non-standard `APCM` chunk instead of `SSND`: raw Green Book ADPCM, 4 bits per
sample at 18,900 Hz -- CD-i Level C, mono. One 128-byte sound group carries a
16-byte parameter block and eight 28-sample sound units, 224 samples in all.

  python tools/cdiaudio.py info [FILE...]
  python tools/cdiaudio.py wav OUTDIR [FILE...]
"""
import sys, os, struct, wave, argparse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_work', 'files')
SAMPLES = os.path.join(ROOT, 'SAMPLES')

F0 = [0, 60, 115, 98, 122]
F1 = [0, 0, -52, -55, -60]


def ext80(b):
    """80-bit IEEE extended -> float."""
    e = struct.unpack('>H', b[0:2])[0]
    m = struct.unpack('>Q', b[2:10])[0]
    if e == 0 and m == 0:
        return 0.0
    return (m / (1 << 63)) * (2.0 ** ((e & 0x7FFF) - 16383))


def chunks(b):
    assert b[0:4] == b'FORM' and b[8:12] == b'AIFF', 'not AIFF-C'
    out, off = [], 12
    while off + 8 <= len(b):
        cid = b[off:off + 4]
        n = struct.unpack('>I', b[off + 4:off + 8])[0]
        out.append((cid.decode('latin-1'), off, n, b[off + 8:off + 8 + n]))
        off += 8 + n + (n & 1)
    return out


def parse(path):
    b = open(path, 'rb').read()
    info = {'size': len(b), 'chunks': []}
    for cid, off, n, data in chunks(b):
        info['chunks'].append((cid, off, n))
        if cid == 'COMM':
            info['channels'] = struct.unpack('>H', data[0:2])[0]
            info['frames'] = struct.unpack('>I', data[2:6])[0]
            info['bits'] = struct.unpack('>H', data[6:8])[0]
            info['rate'] = ext80(data[8:18])
        elif cid == 'APCM':
            info['offset'] = struct.unpack('>I', data[0:4])[0]
            info['blocksize'] = struct.unpack('>I', data[4:8])[0]
            info['adpcm'] = data[8:]
    return info


def decode_group(g, hist):
    """One 128-byte sound group -> 224 mono samples (Level B/C, 4 bit)."""
    out = []
    for u in range(8):
        # header bytes 0-3 hold units 0-3 and 8-11 hold units 4-7;
        # bytes 4-7 and 12-15 repeat them, which is how the layout was confirmed
        sp = g[u] if u < 4 else g[8 + (u - 4)]
        rng = sp & 0x0F
        flt = (sp >> 4) & 0x0F
        if flt > 4:
            flt = 0
        for t in range(28):
            byte = g[16 + t * 4 + (u & 3)]
            nib = (byte >> 4) if u >= 4 else (byte & 0x0F)
            s = (nib ^ 8) - 8                       # sign-extend 4 bits
            v = (s << 12) >> rng
            v += (F0[flt] * hist[0] + F1[flt] * hist[1]) >> 6
            v = max(-32768, min(32767, v))
            hist[1], hist[0] = hist[0], v
            out.append(v)
    return out


def decode(adpcm):
    hist = [0, 0]
    pcm = []
    for o in range(0, len(adpcm) - 127, 128):
        pcm += decode_group(adpcm[o:o + 128], hist)
    return pcm


def write_wav(path, pcm, rate):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(int(round(rate)))
        w.writeframes(struct.pack('<%dh' % len(pcm), *pcm))


def files(args):
    if args:
        return [a if os.path.exists(a) else os.path.join(SAMPLES, a) for a in args]
    return [os.path.join(SAMPLES, f) for f in sorted(os.listdir(SAMPLES))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('rest', nargs='*')
    a = ap.parse_args()
    if a.cmd == 'info':
        print(f'{"file":<22}{"bytes":>7}{"frames":>9}{"rate":>8}{"ch":>3}{"bits":>5}'
              f'{"groups":>8}{"seconds":>8}  chunks')
        for p in files(a.rest):
            i = parse(p)
            g = len(i['adpcm']) // 128
            print(f'{os.path.basename(p):<22}{i["size"]:>7}{i["frames"]:>9}'
                  f'{i["rate"]:>8.0f}{i["channels"]:>3}{i["bits"]:>5}{g:>8}'
                  f'{i["frames"] / i["rate"]:>8.2f}  '
                  + ' '.join(f'{c}({n})' for c, _, n in i['chunks']))
    elif a.cmd == 'wav':
        outdir = a.rest[0]
        os.makedirs(outdir, exist_ok=True)
        for p in files(a.rest[1:]):
            i = parse(p)
            pcm = decode(i['adpcm'])[:i['frames']]
            out = os.path.join(outdir, os.path.basename(p) + '.wav')
            write_wav(out, pcm, i['rate'])
            print(f'{out}  {len(pcm)} samples')


if __name__ == '__main__':
    main()
