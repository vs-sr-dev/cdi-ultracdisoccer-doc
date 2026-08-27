"""Strings out of /CMDS/cdi_demo, split into buckets that mean something.

68000 object code produces a lot of accidental ASCII, so the default view
keeps only runs that look like language: disc paths, sentences, identifiers.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', '_work', 'files', 'CMDS', 'cdi_demo')

PATH = re.compile(r'^/[A-Za-z0-9_./]+$')
WORDY = re.compile(r'[A-Za-z]{3,}')


def runs(b, minlen=5):
    return [(m.start(), m.group().decode('latin-1'))
            for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, b)]


def looks_real(s):
    letters = sum(c.isalpha() or c in ' ._/-' for c in s)
    if letters / len(s) < 0.75:
        return False
    words = WORDY.findall(s)
    return bool(words) and sum(len(w) for w in words) >= max(4, len(s) * 0.4)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    b = open(path, 'rb').read()
    paths, text = [], []
    for o, s in runs(b):
        s = s.strip()
        if not s:
            continue
        if PATH.match(s):
            paths.append((o, s))
        elif looks_real(s):
            text.append((o, s))
    print(f'== {len(paths)} disc paths ==')
    for o, s in paths:
        print(f'{o:06x}  {s}')
    print(f'\n== {len(text)} text runs ==')
    for o, s in text:
        print(f'{o:06x}  {s}')


if __name__ == '__main__':
    main()
