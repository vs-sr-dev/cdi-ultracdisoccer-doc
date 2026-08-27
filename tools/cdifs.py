"""List / extract the CD-i volume.

  python tools/cdifs.py list            full listing, disc order
  python tools/cdifs.py tree            hierarchy
  python tools/cdifs.py extract DIR     write every file out
  python tools/cdifs.py map             sector map of the whole track
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cdilib


def fmt_date(d):
    y, mo, da, h, mi, s = d
    return f'{1900 + y:04d}-{mo:02d}-{da:02d} {h:02d}:{mi:02d}:{s:02d}'


def cmd_list(disc):
    ents = sorted(cdilib.walk(disc), key=lambda e: (e.lba, e.name))
    print(f'{"LBA":>6} {"sectors":>7} {"size":>9}  {"attr":<9} {"#":>2}  {"date":<19}  path')
    for e in ents:
        print(f'{e.lba:6d} {e.nsectors:7d} {e.size:9d}  0x{e.attr:04x}    {e.filenum:2d}  '
              f'{fmt_date(e.date):<19}  {e.path}{"/" if e.is_dir else ""}')


def cmd_tree(disc):
    ents = cdilib.walk(disc)
    for e in ents:
        depth = e.path.count('/') - 1
        print('  ' * depth + e.name + ('/' if e.is_dir else f'  ({e.size:,} B @ {e.lba})'))


def cmd_extract(disc, outdir):
    """Write every file out.

    The volume has a root file `intro_gfx` and a root directory `INTRO_GFX`,
    which are distinct on CD-i and the same name on a case-insensitive host.
    Files that would collide get a `.file` suffix rather than being dropped.
    """
    ents = cdilib.walk(disc)
    dirs = {e.path.lower() for e in ents if e.is_dir}
    for e in ents:
        rel = e.path.lstrip('/')
        if not e.is_dir and e.path.lower() in dirs:
            rel += '.file'
        dst = os.path.join(outdir, rel)
        if e.is_dir:
            os.makedirs(dst, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
        with open(dst, 'wb') as fh:
            fh.write(disc.read(e.lba, e.size))
        print(f'{e.size:9d}  {rel}')


def cmd_map(disc):
    ents = [e for e in cdilib.walk(disc) if not e.is_dir]
    owner = {}
    for e in ents:
        for i in range(e.nsectors):
            owner.setdefault(e.lba + i, e.path)
    run_start, run_key = 0, None
    for lba in range(disc.nsectors + 1):
        sm = disc.raw(lba)[cdilib.HDR + 2] if lba < disc.nsectors else None
        key = (owner.get(lba, '<free>'), sm)
        if key != run_key:
            if run_key is not None:
                print(f'{run_start:6d}-{lba - 1:<6d} {lba - run_start:5d}  '
                      f'{cdilib.submode_str(run_key[1]):<22} {run_key[0]}')
            run_start, run_key = lba, key


if __name__ == '__main__':
    d = cdilib.Disc()
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'list':
        cmd_list(d)
    elif cmd == 'tree':
        cmd_tree(d)
    elif cmd == 'extract':
        cmd_extract(d, sys.argv[2])
    elif cmd == 'map':
        cmd_map(d)
