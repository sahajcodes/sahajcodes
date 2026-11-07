# Licenses & Attributions

Everything in this profile is self-contained: fonts, icons and images are embedded directly in each SVG.

## Fonts (SIL Open Font License 1.1)

| Font | Use | Copyright | Licence text |
| :-- | :-- | :-- | :-- |
| **Instrument Serif** (Regular, Italic) | Display typography | © 2022 The Instrument Serif Project Authors — https://github.com/Instrument/instrument-serif | [`licenses/OFL-InstrumentSerif.txt`](licenses/OFL-InstrumentSerif.txt) |
| **JetBrains Mono** (Regular, Bold) | Technical / monospace typography | © 2020 The JetBrains Mono Project Authors — https://github.com/JetBrains/JetBrainsMono | [`licenses/OFL-JetBrainsMono.txt`](licenses/OFL-JetBrainsMono.txt) |

Modifications: each font was subset (Basic Latin plus a handful of punctuation glyphs), hinting was removed,
and the result was repackaged as WOFF2 and base64-embedded in the SVGs (`assets/fonts/*.subset.woff2`).
Neither font declares a Reserved Font Name. The OFL permits embedding, subsetting and redistribution.

> Note: the Instrument Serif OFL file here uses the standard OFL 1.1 text with the copyright line copied
> from the font's own metadata (name table ID 0). If you want the upstream file verbatim, grab `OFL.txt`
> from the Instrument Serif repository above.

## Brand icons

| Icon(s) | Source | Licence |
| :-- | :-- | :-- |
| C++, Python, JavaScript, HTML5, CSS (CSS3 slot), Flask, Bootstrap, Git, GitHub, LeetCode | [Simple Icons](https://simpleicons.org) (as shipped in `react-icons` 5.7.0, `react-icons/si`) | CC0 1.0 (icon artwork). Brand marks remain trademarks of their owners. |
| VS Code | Codicons `vscode` glyph (`react-icons/vsc`) — **not** the Simple Icons `vscodium` mark, which is a different product | CC BY 4.0, © Microsoft Corporation |
| LinkedIn | Font Awesome Free 6 brands (`react-icons/fa6`) — Simple Icons no longer carries LinkedIn | CC BY 4.0, © Fonticons, Inc. |
| `react-icons` packaging | https://github.com/react-icons/react-icons | MIT |

Notes:
- Simple Icons removed the old CSS3 shield; its current **CSS** mark is used for the "CSS3" label.
- Icons are drawn monochrome in the Cherry × Matcha palette; the shapes are the unmodified official glyphs.
- All trademarks (C++, Python, JavaScript, HTML5, CSS, Flask, Bootstrap, Git, GitHub, LeetCode, VS Code, LinkedIn)
  belong to their respective owners and are used only to identify the technologies.

## Images

`assets/img/id.jpg` and `assets/img/right_pointing.png` are personal photographs/artwork supplied by the profile owner.
They are embedded byte-for-byte (SHA-256 verified) and are **not** covered by any open licence — all rights reserved.

## Palette

Cherry `#670626`, Matcha `#BAD797` (from the supplied reference), plus Deep Cherry `#3D071A`, Soft Ivory `#F7F3E8`,
Muted Sage `#8FAE75`, Dusty Rose `#D9A6AD`, Warm Taupe `#B9AE9B`.
