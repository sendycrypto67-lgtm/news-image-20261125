"""The World Today, Wednesday 25 November 2026. Pure Python, stdlib only."""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (18, 28, 44)
NAVY = (15, 42, 74)
NAVY2 = (22, 58, 96)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 120, 110)
BLUE = (38, 110, 180)
SKY = (135, 190, 230)
WHITE = (255, 255, 255)
GREY = (90, 98, 110)
LIGHT = (232, 236, 240)
CARD = (255, 255, 255)
GREEN = (46, 139, 87)
ORANGE = (224, 122, 26)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def line(self, x0, y0, x1, y1, c, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(thick):
                for b in range(thick):
                    self.set(x + a, y + b, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def triangle(self, pts, c):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            inter = []
            for i in range(3):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % 3]
                if y0 == y1:
                    continue
                if min(y0, y1) <= yy < max(y0, y1):
                    inter.append(x0 + (yy - y0) * (x1 - x0) / (y1 - y0))
            if len(inter) >= 2:
                inter.sort()
                for xx in range(int(inter[0]), int(inter[-1]) + 1):
                    self.set(xx, yy, c)

    def text(self, x, y, s, scale, c):
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[" "])
            for r in range(7):
                for col in range(5):
                    if g[r][col] == "1":
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + col * scale + dx, y + r * scale + dy, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def centred(self, y, s, scale, c):
        self.text((W - self.text_w(s, scale)) // 2, y, s, scale, c)


def wrap(canvas, s, scale, max_w):
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if canvas.text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_hero_art(cv):
    # Night sky panel on the right of the hero, fully inside the hero card.
    cv.rect(588, 140, 404, 318, NAVY)
    for (sx, sy) in [(620, 165), (700, 155), (760, 180), (880, 160), (940, 200),
                     (650, 230), (920, 260), (700, 300), (840, 320), (960, 340)]:
        cv.circle(sx, sy, 2, WHITE)
    # Earth, fully inside the panel: centre (860, 385), radius 62.
    cv.circle(860, 385, 62, BLUE)
    cv.circle(840, 365, 20, GREEN)
    cv.circle(880, 400, 16, GREEN)
    cv.circle(862, 340, 12, GREEN)
    # Satellite: body, panels, dish, antenna.
    cv.rect(700, 210, 90, 44, LIGHT)
    cv.rect(700, 210, 90, 8, GREY)
    cv.rect(610, 220, 84, 26, (52, 110, 190))
    cv.rect(796, 220, 84, 26, (52, 110, 190))
    cv.line(694, 233, 610, 233, GREY, 3)
    cv.line(790, 233, 886, 233, GREY, 3)
    cv.circle(745, 232, 12, GOLD)
    cv.line(745, 210, 745, 178, WHITE, 3)
    cv.circle(745, 172, 7, RED)
    cv.line(790, 250, 830, 285, WHITE, 2)
    cv.text(612, 168, "SATELLITE", 2, WHITE)
    cv.text(612, 420, "EARTH", 2, WHITE)


def draw_ship(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    cv.rect(x + 18, y + h - 42, w - 36, 26, (30, 60, 90))
    cv.triangle([(x + 18, y + h - 16), (x + w - 18, y + h - 16), (x + w - 30, y + h)], (30, 60, 90))
    for i, col in enumerate([RED, GOLD, TEAL, ORANGE]):
        cv.rect(x + 30 + i * 52, y + 22, 46, 30, col)
    cv.rect(x + w - 66, y + 8, 44, 22, WHITE)
    cv.line(x + 20, y + h - 52, x + w - 20, y + h - 52, INK, 2)
    cv.line(x + 30, y + h - 20, x + 90, y + 14, RED, 3)
    cv.line(x + 90, y + 14, x + 150, y + 34, RED, 3)
    cv.line(x + 150, y + 34, x + 210, y + 18, RED, 3)


def draw_summit(cv, x, y, w, h):
    cv.rect(x, y, w, h, (214, 228, 238))
    cv.triangle([(x + 20, y + 30), (x + w // 2, y + 4), (x + w - 20, y + 30)], NAVY2)
    cv.rect(x + 30, y + 30, w - 60, h - 34, (240, 236, 220))
    for i in range(5):
        cv.rect(x + 44 + i * 46, y + 36, 28, 12, NAVY2)
    for i, col in enumerate([RED, TEAL, GOLD, BLUE, GREEN]):
        cv.line(x + 40 + i * 48, y + 28, x + 40 + i * 48, y + 10, INK, 2)
        cv.rect(x + 40 + i * 48, y + 10, 18, 10, col)
    cv.circle(x + w - 30, y + 16, 8, GOLD)


def draw_skyline(cv, x, y, w, h):
    cv.rect(x, y, w, h, (18, 32, 56))
    for i, bh in enumerate([28, 42, 24, 48, 32, 38]):
        bx = x + 14 + i * 48
        cv.rect(bx, y + h - 6 - bh, 38, bh, (70, 90, 120))
        for wy in range(y + h - bh, y + h - 10, 12):
            for wx in range(bx + 6, bx + 32, 12):
                cv.set(wx, wy, GOLD)
                cv.set(wx + 1, wy, GOLD)
    cv.circle(x + w - 36, y + 14, 8, WHITE)


def draw_flags(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    cv.line(x + 42, y + 10, x + 42, y + h - 8, INK, 3)
    cv.line(x + w - 42, y + 10, x + w - 42, y + h - 8, INK, 3)
    cv.rect(x + 46, y + 12, 84, 44, (0, 40, 110))
    cv.rect(x + 46, y + 12, 34, 22, (200, 30, 30))
    cv.circle(x + 100, y + 40, 5, WHITE)
    cv.rect(x + w - 130, y + 12, 84, 44, (0, 90, 160))
    cv.rect(x + w - 130, y + 34, 84, 22, GREEN)
    for (fx, fy) in [(x + w - 110, y + 22), (x + w - 80, y + 24), (x + w - 95, y + 46)]:
        cv.circle(fx, fy, 3, GOLD)
    cv.circle(x + w // 2, y + h - 22, 16, (240, 200, 160))
    cv.rect(x + w // 2 - 34, y + h - 30, 30, 14, (240, 200, 160))
    cv.rect(x + w // 2 + 4, y + h - 30, 30, 14, (200, 170, 130))


def draw_rocket(cv, x, y, w, h):
    cv.rect(x, y, w, h, NAVY)
    for (sx, sy) in [(x + 20, y + 14), (x + 70, y + 10), (x + 230, y + 16), (x + 260, y + 40), (x + 40, y + 50)]:
        cv.circle(sx, sy, 2, WHITE)
    cx = x + w // 2
    cv.rect(cx - 22, y + 24, 44, 40, WHITE)
    cv.triangle([(cx - 22, y + 24), (cx + 22, y + 24), (cx, y + 4)], RED)
    cv.circle(cx, y + 42, 8, SKY)
    cv.triangle([(cx - 22, y + 64), (cx - 38, y + 74), (cx - 22, y + 72)], RED)
    cv.triangle([(cx + 22, y + 64), (cx + 38, y + 74), (cx + 22, y + 72)], RED)
    cv.triangle([(cx - 12, y + 64), (cx + 12, y + 64), (cx, y + 76)], GOLD)
    cv.circle(x + 34, y + 26, 14, (220, 220, 220))


def build():
    cv = Canvas(W, H, PAPER)
    # Masthead.
    cv.rect(0, 0, W, 118, NAVY)
    cv.rect(0, 118, W, 6, GOLD)
    cv.centred(14, "THE WORLD TODAY", 5, WHITE)
    cv.centred(62, "WEDNESDAY 25 NOVEMBER 2026", 2, GOLD)
    cv.centred(88, "SIX STORIES FROM ONE DAY, AROUND THE WORLD", 2, WHITE)
    # Hero.
    cv.rect(24, 136, 968, 330, CARD)
    cv.rect(24, 136, 968, 4, RED)
    cv.text(44, 158, "TOP STORY", 2, RED)
    cv.text(44, 182, "NATO VOWS TO", 4, INK)
    cv.text(44, 218, "DEFEND SPACE", 4, INK)
    hero = wrap(cv, "Alliance answers reports Russia is preparing a nuclear-armed satellite launch, possibly as soon as December.", 2, 520)
    yy = 268
    for ln in hero:
        cv.text(44, yy, ln, 2, INK)
        yy += 26
    # (No extra hero line: only facts verified in the 25 Nov research are shown.)
    draw_hero_art(cv)
    # Grid: three cards, then two wide cards.
    cards = [
        ("TARIFFS", "NEW TARIFFS LOOM", "Duties planned on 16 trading partners after an excess-capacity probe; Asian markets slide.", draw_ship),
        ("CLIMATE", "CLIMATE SUMMIT ENDS WITHOUT A DEAL", "COP31 in Antalya ends with no deal among more than 190 countries.", draw_summit),
        ("CHINA", "SHANGHAI CHIEF UNDER PROBE", "Beijing opens a corruption inquiry into Shanghai Party chief Chen Jining.", draw_skyline),
        ("PACIFIC", "PACIFIC SECURITY PACT", "Australia and Solomon Islands sign a security deal; Australia named primary security partner.", draw_flags),
        ("SPACE", "SHENZHOU-24 LIFTS OFF", "China launches a crewed mission carrying a Pakistani astronaut.", draw_rocket),
    ]
    # Row 1: three cards.
    for i in range(3):
        kicker, head, summ, art = cards[i]
        x = 24 + i * 328
        y = 482
        cv.rect(x, y, 312, 224, CARD)
        cv.rect(x, y, 312, 4, NAVY2)
        art(cv, x + 8, y + 8, 296, 58)
        cv.text(x + 12, y + 74, kicker, 2, RED)
        lines = wrap(cv, head, 2, 288)
        hy = y + 96
        for ln in lines[:2]:
            cv.text(x + 12, hy, ln, 2, INK)
            hy += 22
        slines = wrap(cv, summ, 2, 288)
        sy = hy + 4
        max_lines = max(1, (y + 224 - sy) // 20)
        for ln in slines[:max_lines]:
            cv.text(x + 12, sy, ln, 2, INK)
            sy += 20
    # Row 2: two wide cards.
    for j in range(2):
        kicker, head, summ, art = cards[3 + j]
        x = 24 + j * 496
        y = 722
        cv.rect(x, y, 480, 224, CARD)
        cv.rect(x, y, 480, 4, TEAL)
        art(cv, x + 8, y + 10, 464, 76)
        cv.text(x + 12, y + 96, kicker, 2, RED)
        cv.text(x + 12, y + 118, head, 2, INK)
        slines = wrap(cv, summ, 2, 456)
        sy = y + 148
        for ln in slines[:3]:
            cv.text(x + 12, sy, ln, 2, INK)
            sy += 22
    # Footer.
    cv.rect(0, 962, W, 62, NAVY)
    cv.centred(978, "NATO, TRADE, CLIMATE, CHINA, THE PACIFIC AND SPACE", 2, WHITE)
    cv.centred(1002, "WEDNESDAY 25 NOVEMBER 2026", 2, GOLD)
    return cv


def png_bytes(cv):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(cv.px[y * W * 3:(y + 1) * W * 3])

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    return png


def validate_png(data):
    """Check PNG structure: signature, per-chunk CRCs, IEND last, no trailing bytes."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    pos = 8
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            raise ValueError("truncated chunk " + kind.decode("latin1"))
        stored = struct.unpack(">I", data[end - 4:end])[0]
        actual = zlib.crc32(kind + data[pos + 8:pos + 8 + length]) & 0xFFFFFFFF
        if stored != actual:
            raise ValueError("CRC mismatch in " + kind.decode("latin1"))
        pos = end
        if kind == b"IEND":
            seen_iend = True
            break
    if not seen_iend:
        raise ValueError("missing IEND chunk")
    if pos != len(data):
        raise ValueError("trailing bytes after IEND")
    if len(data) > 1048576:
        raise ValueError("PNG over 1 MiB")
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build())
    validate_png(data)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
