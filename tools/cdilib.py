"""Shared helpers for the Ultra CD-i Soccer disc.

The disc is a single MODE2/2352 track. Every sector carries a 16-byte
sync+header, an 8-byte subheader (stored twice), then either 2048 bytes
(Form 1) or 2324 bytes (Form 2) of user data.
"""
import os, struct

RAW = 2352
HDR = 16          # sync(12) + header(4)
SUBHDR = 4        # file, channel, submode, coding -- stored twice
USER = HDR + 2 * SUBHDR   # 24: start of user data

SM_EOR, SM_VIDEO, SM_AUDIO, SM_DATA = 0x01, 0x02, 0x04, 0x08
SM_TRIGGER, SM_FORM2, SM_RT, SM_EOF = 0x10, 0x20, 0x40, 0x80

DEFAULT_BIN = os.path.join(os.path.dirname(__file__), '..', '_work', 'ultrasoccer.bin')


class Disc:
    def __init__(self, path=None):
        self.path = os.path.abspath(path or DEFAULT_BIN)
        self.f = open(self.path, 'rb')
        self.nsectors = os.path.getsize(self.path) // RAW

    def raw(self, lba):
        self.f.seek(lba * RAW)
        return self.f.read(RAW)

    def subheader(self, lba):
        s = self.raw(lba)
        return s[HDR:HDR + 4]           # file, channel, submode, coding

    def data(self, lba):
        """User data of one sector, sized by the Form bit in the subheader."""
        s = self.raw(lba)
        submode = s[HDR + 2]
        n = 2324 if (submode & SM_FORM2) else 2048
        return s[USER:USER + n]

    def read(self, lba, nbytes):
        out = bytearray()
        while len(out) < nbytes:
            out += self.data(lba)
            lba += 1
        return bytes(out[:nbytes])


def submode_str(sm):
    names = [(SM_EOF, 'EOF'), (SM_RT, 'RT'), (SM_FORM2, 'F2'), (SM_TRIGGER, 'TRIG'),
             (SM_DATA, 'DATA'), (SM_AUDIO, 'AUDIO'), (SM_VIDEO, 'VIDEO'), (SM_EOR, 'EOR')]
    return '|'.join(n for b, n in names if sm & b) or '-'


# ---------------------------------------------------------------- filesystem

ATTR_BITS = [(0, 'owner-read'), (2, 'owner-exec'), (4, 'group-read'), (6, 'group-exec'),
             (8, 'world-read'), (10, 'world-exec'), (12, 'cdda'), (15, 'directory')]


def attr_str(a):
    return ','.join(n for b, n in ATTR_BITS if a & (1 << b)) or '-'


class Entry:
    __slots__ = ('name', 'lba', 'size', 'date', 'flags', 'unit', 'gap',
                 'attr', 'owner', 'filenum', 'parent', 'is_dir')

    @property
    def path(self):
        return (self.parent + '/' + self.name).replace('//', '/')

    @property
    def nsectors(self):
        return (self.size + 2047) // 2048

    def __repr__(self):
        return f'<{self.path} lba={self.lba} size={self.size}>'


def parse_dir(buf, parent):
    """Yield Entry records out of a raw CD-i directory extent."""
    off = 0
    while off < len(buf):
        ln = buf[off]
        if ln == 0:                     # rest of this 2048-byte block is padding
            off = (off // 2048 + 1) * 2048
            continue
        r = buf[off:off + ln]
        e = Entry()
        e.lba = struct.unpack('>I', r[6:10])[0]
        e.size = struct.unpack('>I', r[14:18])[0]
        e.date = tuple(r[18:24])
        e.flags = r[25]
        e.unit, e.gap = r[26], r[27]
        nl = r[32]
        e.name = r[33:33 + nl].decode('latin-1')
        sysoff = 33 + nl + (1 - (nl & 1))
        su = r[sysoff:sysoff + 10]
        e.owner = struct.unpack('>HH', su[0:4]) if len(su) >= 4 else (0, 0)
        e.attr = struct.unpack('>H', su[4:6])[0] if len(su) >= 6 else 0
        e.filenum = su[8] if len(su) >= 9 else 0
        e.is_dir = bool(e.attr & 0x8000)
        e.parent = parent
        if nl == 1 and e.name in ('\x00', '\x01'):
            e.name = '.' if e.name == '\x00' else '..'
        yield e
        off += ln


def walk(disc, root_lba=None, root_size=None):
    """Depth-first walk of the whole volume. Returns a flat list of Entry."""
    if root_lba is None:
        vd = disc.read(16, 2048)
        pt_lba = struct.unpack('>I', vd[148:152])[0]
        pt_size = struct.unpack('>I', vd[136:140])[0]
        pt = disc.read(pt_lba, pt_size)
        root_lba = struct.unpack('>I', pt[2:6])[0]
        root_size = 2048
    out = []

    def rec(lba, size, parent):
        buf = disc.read(lba, size)
        for e in parse_dir(buf, parent):
            if e.name in ('.', '..'):
                continue
            out.append(e)
            if e.is_dir:
                rec(e.lba, e.size, e.path)

    # the root extent's own '.' record carries the true directory size
    first = next(parse_dir(disc.read(root_lba, 2048), '/'))
    rec(root_lba, first.size, '')
    return out


def volume_info(disc):
    vd = disc.read(16, 2048)
    g = lambda a, b: vd[a:b].decode('latin-1').rstrip()
    return dict(
        std_id=g(1, 6), system_id=g(8, 40), volume_id=g(40, 72),
        volume_size=struct.unpack('>I', vd[84:88])[0],
        block_size=struct.unpack('>H', vd[130:132])[0],
        path_table_size=struct.unpack('>I', vd[136:140])[0],
        path_table_lba=struct.unpack('>I', vd[148:152])[0],
        volume_set=g(190, 318), publisher=g(318, 446),
        data_preparer=g(446, 574), application=g(574, 702),
        copyright_file=g(702, 739), abstract_file=g(739, 776),
        biblio_file=g(776, 813), created=g(813, 830),
    )
