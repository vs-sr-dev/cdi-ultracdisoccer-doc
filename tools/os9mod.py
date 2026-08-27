"""Parse the OS-9/68000 modules inside /CMDS/cdi_demo.

CD-i runs CD-RTOS, Philips' OS-9 version 2.4 derivative. Every executable is
one or more relocatable modules, each starting with the $4AFC sync word and
ending with a CRC-24 over the whole module.
"""
import sys, struct, os

TYPES = {0: 'Devic?', 1: 'Prgrm', 2: 'Sbrtn', 3: 'Multi', 4: 'Data', 5: 'CSDData',
         11: 'Trap', 12: 'Systm', 13: 'FlMgr', 14: 'Drivr', 15: 'Devic'}
LANGS = {0: 'Objct', 1: '68000 object', 2: 'ICode', 3: 'PCode', 4: 'CCode',
         5: 'CblCode', 6: 'FrtnCode'}
ATTRS = [(7, 'reentrant'), (6, 'ghost'), (5, 'sticky'), (4, 'system-state')]


def crc24(data):
    """OS-9 module CRC: poly $800063, preset $FFFFFF, no final xor."""
    acc = 0xFFFFFF
    for b in data:
        acc ^= b << 16
        for _ in range(8):
            acc <<= 1
            if acc & 0x1000000:
                acc ^= 0x800063
    return acc & 0xFFFFFF


def header_parity(data):
    """M$Parity is the XOR of the 24 header words, complemented."""
    p = 0
    for i in range(0, 46, 2):
        p ^= struct.unpack('>H', data[i:i + 2])[0]
    return (~p) & 0xFFFF


def cstr(b, off):
    """OS-9 names have bit 7 set on the last character."""
    out = []
    while off < len(b):
        c = b[off]
        out.append(chr(c & 0x7F))
        if c & 0x80:
            break
        off += 1
    return ''.join(out)


def parse(b, off):
    d = b[off:off + 80]
    m = dict(offset=off)
    m['sysrev'] = struct.unpack('>H', d[2:4])[0]
    m['size'] = struct.unpack('>I', d[4:8])[0]
    m['owner'] = struct.unpack('>I', d[8:12])[0]
    m['name_off'] = struct.unpack('>I', d[12:16])[0]
    m['access'] = struct.unpack('>H', d[16:18])[0]
    m['type'] = d[18]
    m['lang'] = d[19]
    m['attr'] = d[20]
    m['revs'] = d[21]
    m['edit'] = struct.unpack('>H', d[22:24])[0]
    m['usage'] = struct.unpack('>I', d[24:28])[0]
    m['symbol'] = struct.unpack('>I', d[28:32])[0]
    m['parity'] = struct.unpack('>H', d[46:48])[0]
    m['parity_ok'] = m['parity'] == header_parity(d)
    if m['type'] in (1, 2, 3, 11, 12):
        (m['exec'], m['excpt'], m['mem'], m['stack'], m['idata'],
         m['irefs'], m['init'], m['term']) = struct.unpack('>8I', d[48:80])
    body = b[off:off + m['size']]
    m['crc_stored'] = struct.unpack('>I', b'\x00' + body[-3:])[0]
    m['crc_ok'] = crc24(body[:-3]) == (crc24(body) ^ 0) and True
    # OS-9 defines CRC over the whole module including the stored CRC == $800FE3
    m['crc_ok'] = crc24(body) == 0x800FE3
    m['name'] = cstr(b, off + m['name_off'])
    return m


def find_modules(b):
    out, off = [], 0
    while off < len(b) - 1:
        if b[off:off + 2] == b'\x4a\xfc':
            try:
                m = parse(b, off)
            except Exception:
                off += 2
                continue
            if 48 < m['size'] <= len(b) - off and m['parity_ok']:
                out.append(m)
                off += m['size']
                continue
        off += 2
    return out


def show(m):
    print(f"module @ 0x{m['offset']:06x}  '{m['name']}'")
    print(f"  size        {m['size']:,} bytes   sysrev {m['sysrev']}  edition {m['edit']}")
    print(f"  type/lang   {TYPES.get(m['type'], m['type'])} / {LANGS.get(m['lang'], m['lang'])}")
    at = ','.join(n for b_, n in ATTRS if m['attr'] & (1 << b_)) or '-'
    print(f"  attr/rev    0x{m['attr']:02x} ({at}) rev {m['revs']}   access 0x{m['access']:04x}"
          f"   owner {m['owner'] >> 16}.{m['owner'] & 0xffff}")
    print(f"  parity      0x{m['parity']:04x} {'OK' if m['parity_ok'] else 'BAD'}"
          f"   crc24 0x{m['crc_stored']:06x} {'OK' if m['crc_ok'] else 'BAD'}")
    if 'exec' in m:
        print(f"  M$Exec      0x{m['exec']:06x}    M$Excpt 0x{m['excpt']:06x}")
        print(f"  M$Mem       {m['mem']:,} B static   M$Stack {m['stack']:,} B")
        print(f"  M$IData     0x{m['idata']:06x}    M$IRefs 0x{m['irefs']:06x}")
        print(f"  M$Init      0x{m['init']:06x}    M$Term  0x{m['term']:06x}")


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '_work/files/CMDS/cdi_demo'
    b = open(path, 'rb').read()
    mods = find_modules(b)
    print(f'{path}: {len(b):,} bytes, {len(mods)} module(s)\n')
    for m in mods:
        show(m)
        print()
    tail = mods[-1]['offset'] + mods[-1]['size'] if mods else 0
    if tail < len(b):
        print(f'trailing {len(b) - tail} bytes after last module '
              f'(0x{tail:x}..0x{len(b):x})')
