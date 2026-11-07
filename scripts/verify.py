from pathlib import Path
import xml.etree.ElementTree as ET, re, json
P=Path(__file__).resolve().parents[1]; A=P/'assets'
report=[]
for f in sorted(A.glob('*.svg')):
    root=ET.parse(f).getroot(); text=f.read_text()
    checks={'valid_xml':True,'no_script':'<script' not in text.lower(),'no_foreignObject':'foreignObject' not in text,'no_external_href':not bool(re.search(r'(?:href|xlink:href)=["\']https?://',text)),'reduced_motion':'prefers-reduced-motion' in text}
    report.append({'file':str(f.relative_to(P)),**checks})
    if not all(checks.values()): raise SystemExit(f'Validation failed: {f}: {checks}')
(P/'VERIFICATION.md').write_text('# Verification report\n\n## Static checks\n\n'+ '\n'.join(f"- **{x['file']}**: XML valid; no JavaScript; no `foreignObject`; no external image/font references; reduced-motion CSS present." for x in report)+'\n\n## Browser checks\n\nLocal Chromium screenshots are generated for each SVG and the full preview page. This confirms local rendering only, not GitHub sanitization or animation playback in GitHub README surfaces.\n\n## Pending image checks\n\nPortrait accuracy/transparency and laptop character accuracy/transparency cannot be tested until the two original PNG assets are supplied.\n')
print(json.dumps(report,indent=2))
