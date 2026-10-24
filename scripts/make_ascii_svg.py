from pathlib import Path

from PIL import Image, ImageOps


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

INPUT_IMAGE = DATA_DIR / "source-prepped.png"
OUTPUT_SVG = DATA_DIR / "avi-ascii.svg"

# Darker characters represent darker parts of the photo
RAMP = " .`:-=+*cs#%@"


def main():
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError(
            f"Prepared photo not found: {INPUT_IMAGE}\n"
            "Run: python scripts/prep_photo.py"
        )

    print("Loading prepared photo...", flush=True)

    image = Image.open(INPUT_IMAGE).convert("L")

    # Resize while accounting for the height of monospace characters
    columns = 100
    rows = max(1, round(image.height / image.width * columns * 0.52))
    image = ImageOps.fit(image, (columns, rows))
    pixels = list(image.getdata())

    print("Generating ASCII characters...", flush=True)

    lines = []
    for y in range(rows):
        line = ""
        for x in range(columns):
            brightness = pixels[y * columns + x]
            index = round((255 - brightness) / 255 * (len(RAMP) - 1))
            line += RAMP[index]
        lines.append(line)

    # Each row reveals from left to right, with a staggered delay
    svg_parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'viewBox="0 0 1000 530" role="img">',
        '<title>Animated ASCII portrait</title>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>',
        'text { font-family: "Courier New", monospace; '
        'font-size: 10px; white-space: pre; fill: #111; }',
        '</style>',
    ]

    for y, line in enumerate(lines):
        delay = y * 0.035
        svg_parts.append(
            f'<clipPath id="row{y}">'
            f'<rect x="0" y="{y * 10}" width="0" height="10">'
            f'<animate attributeName="width" from="0" to="1000" '
            f'dur="0.7s" begin="{delay:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        svg_parts.append(
            f'<text x="0" y="{(y + 1) * 10}" '
            f'clip-path="url(#row{y})">{escape_xml(line)}</text>'
        )

    svg_parts.append('</svg>')

    OUTPUT_SVG.write_text("\n".join(svg_parts), encoding="utf-8")

    print(f"\nDone! ASCII SVG saved to:\n{OUTPUT_SVG}", flush=True)
    print(f"Grid size: {columns} columns × {rows} rows")


def escape_xml(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


if __name__ == "__main__":
    main()