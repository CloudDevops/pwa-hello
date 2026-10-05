#!/usr/bin/env python3
"""De-brand Dino Valley: remove the Tesla and Cybertruck names from the single-file game.

Usage:
    python3 tools/debrand-dino-valley.py INPUT.html OUTPUT.html   # rewrite
    python3 tools/debrand-dino-valley.py --check FILE.html         # only report brand mentions

What it changes (Dino Valley v17 markers; every marker must be found or the run fails):
  * Start-menu buttons: "Cybertruck" -> "Silver truck", "Red Tesla" -> "Red car" (labels and alt text).
    The in-game ride picker clones these buttons, so it follows automatically.
  * Vehicle type token 'tesla' -> 'redcar' everywhere in code (data-car, thumbnail id, parked-spot id,
    switchRide list, wheel geometry, contact shadows, door colour).
  * Tapping the parked silver truck used to play "C is for Cybertruck" (narration clip 2). The camp sign
    already teaches C with its own clip, so the truck tap now plays the existing "H is for horn" line
    (clip 7) with the label at the truck. No new audio is needed.
  * The unused words list entry 'Cybertruck' -> 'Camp'.

If the input was downloaded from the live ChatGPT Sites host it may carry a Cloudflare bot-challenge
<script> block appended before </body>; that block is not part of the game and is removed when present.

Only code and markup are touched. Base64 asset payloads (images, music, narration) are passed through
byte for byte. The sprite art itself still shows a Cybertruck-shaped truck; that needs new artwork.
"""
import re
import sys

B64 = re.compile(r'data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]+')
BRAND = re.compile(r'cybertruck|tesla', re.IGNORECASE)
CF_INJECT = re.compile(r"<script>\(function\(\)\{function c\(\)\{(?:(?!</script>).)*?(?:__CF\$cv\$params|cdn-cgi/challenge-platform)(?:(?!</script>).)*</script>", re.S)

EXACT = [
    # (old, new, expected occurrences)
    ('<img id="truckThumb" alt="Silver Cybertruck">Cybertruck</button>',
     '<img id="truckThumb" alt="Silver pickup truck">Silver truck</button>', 1),
    ('<button class="car" data-car="tesla" aria-pressed="false"><img id="teslaThumb" alt="Red Tesla">Red Tesla</button>',
     '<button class="car" data-car="redcar" aria-pressed="false"><img id="redcarThumb" alt="Red car">Red car</button>', 1),
    ("words=['Apple','Ball','Cybertruck',", "words=['Apple','Ball','Camp',", 1),
    ("case'truck':learn(2,'C is for Cybertruck. Beep beep!',s.x,s.y);honk(false);break;",
     "case'truck':learn(7,'H is for horn. Beep beep!',s.x,s.y);honk(false);break;", 1),
    ("['truckThumb',0],['teslaThumb',1]", "['truckThumb',0],['redcarThumb',1]", 1),
    ("id:'parkedtesla',vehicleType:'tesla'", "id:'parkedredcar',vehicleType:'redcar'", 1),
    ("['truck','tesla','dump','excavator']", "['truck','redcar','dump','excavator']", 1),
    ("type==='tesla'", "type==='redcar'", 3),  # wheel geometry, contact shadows, door colour
]


def split_segments(text):
    """Yield (is_asset, chunk) so replacements never touch base64 payloads."""
    pos = 0
    for m in B64.finditer(text):
        if m.start() > pos:
            yield False, text[pos:m.start()]
        yield True, m.group(0)
        pos = m.end()
    if pos < len(text):
        yield False, text[pos:]


def brand_mentions(code):
    out = []
    for m in BRAND.finditer(code):
        a, b = max(0, m.start() - 60), min(len(code), m.end() + 60)
        out.append((m.group(0), code[a:b].replace('\n', ' ')))
    return out


def main(argv):
    if len(argv) == 3 and argv[1] == '--check':
        text = open(argv[2], encoding='utf-8').read()
        code = ''.join(chunk for is_asset, chunk in split_segments(text) if not is_asset)
        hits = brand_mentions(code)
        print(f'{argv[2]}: {len(hits)} brand mention(s) in code/markup, '
              f'{len(text) - len(code)} bytes of assets skipped')
        for word, ctx in hits:
            print(f'  [{word}] ...{ctx}...')
        return 0 if not hits else 1
    if len(argv) != 3:
        print(__doc__)
        return 2

    src, dst = argv[1], argv[2]
    text = open(src, encoding='utf-8').read()
    segments = list(split_segments(text))
    code = ''.join(chunk for is_asset, chunk in segments if not is_asset)
    assets = sum(len(chunk) for is_asset, chunk in segments if is_asset)
    before = len(brand_mentions(code))

    problems = []
    for old, new, expected in EXACT:
        n = code.count(old)
        if n != expected:
            problems.append(f'expected {expected} x {old[:60]!r}, found {n}')
    if problems:
        print('Markers do not match this file; nothing written:')
        for p in problems:
            print('  -', p)
        return 1

    for old, new, expected in EXACT:
        code = code.replace(old, new)
        print(f'  {expected} x {old[:58]!r} -> {new[:58]!r}')
    cf = CF_INJECT.findall(code)
    if cf:
        code = CF_INJECT.sub('', code)
        print(f'  removed {len(cf)} Cloudflare challenge <script> block(s) injected by the live host')

    left = brand_mentions(code)
    if left:
        print('Brand mentions still present after rewrite; nothing written:')
        for word, ctx in left:
            print(f'  [{word}] ...{ctx}...')
        return 1

    # Reassemble: apply the same replacements per code chunk so assets stay byte for byte.
    rebuilt = []
    for is_asset, chunk in segments:
        if is_asset:
            rebuilt.append(chunk)
            continue
        c = chunk
        for old, new, _ in EXACT:
            c = c.replace(old, new)
        c = CF_INJECT.sub('', c)
        rebuilt.append(c)
    result = ''.join(rebuilt)
    if ''.join(ch for is_asset, ch in split_segments(result) if not is_asset) != code:
        print('Internal consistency check failed; nothing written.')
        return 1

    with open(dst, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'wrote {dst}: {len(result):,} bytes; brand mentions {before} -> 0; '
          f'{assets:,} asset bytes unchanged')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
