from pathlib import Path
import sys
BAD=["\\u00c3","\\u00c2","\\u00e2\\u20ac","\\u00ef\\u00bf\\u00bd","\\ufffd"]
ROOT=Path(__file__).resolve().parents[1]
exts={".md",".txt",".json",".yml",".yaml",".py"}
fails=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in exts:
        continue
    try:
        t=p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fails.append(f"{p.relative_to(ROOT)}: invalid UTF-8"); continue
    for raw in BAD:
        marker=raw.encode().decode("unicode_escape")
        if marker in t:
            fails.append(f"{p.relative_to(ROOT)}: possible mojibake")
if fails:
    print("PUBLIC CONTENT QUALITY: FAIL")
    print("\n".join(fails))
    sys.exit(1)
print("PUBLIC CONTENT QUALITY: PASS")
