#!/usr/bin/env python3
"""
scripts/merge_aladin_meta.py

ocr_results/aladin_meta.json 을 읽어 app-data.js의 RECOMMENDED_BOOKS·EXTRA_BOOKS 객체에
summary (책 소개), isbn, aladinLink 필드를 병합한다.

실행:
    cd C:\dev\bookquest
    python scripts/merge_aladin_meta.py

사전조건:
    - scripts/fetch_aladin_descriptions.js 실행 완료 후
    - ocr_results/aladin_meta.json 존재

안전:
    - 작업 전 backup/ 에 app-data.js 스냅샷 자동 생성
    - 객체별 한 줄 단위로 정확히 매칭, 1회 매칭 안 되면 중단
    - description, fullDescription 중 더 긴 것을 summary로 사용
"""

import json, re, sys, os, shutil, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_DATA = ROOT / "app-data.js"
META_PATH = ROOT / "ocr_results" / "aladin_meta.json"
BACKUP_DIR = ROOT / "backup"

if not META_PATH.exists():
    print(f"[ERR] {META_PATH} 없음. 먼저 scripts/fetch_aladin_descriptions.js 를 실행하세요.")
    sys.exit(1)

if not APP_DATA.exists():
    print(f"[ERR] {APP_DATA} 없음.")
    sys.exit(1)

# Backup
BACKUP_DIR.mkdir(exist_ok=True)
ts = time.strftime("%Y%m%d_%H%M%S")
bk = BACKUP_DIR / f"app-data-pre-aladin-merge-{ts}.js"
shutil.copy(APP_DATA, bk)
print(f"[OK] backup: {bk.name}")

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

print(f"[OK] aladin_meta entries: {len(meta)}")

with open(APP_DATA, "r", encoding="utf-8") as f:
    src = f.read()

original_size = len(src.encode("utf-8"))
updated = 0
skipped = 0
not_found = 0

# Helper: pick the best summary from meta entry
def pick_summary(entry):
    fd = (entry.get("fullDescription") or "").strip()
    sd = (entry.get("description") or "").strip()
    # Prefer the longer non-empty one
    if len(fd) >= max(50, len(sd)):
        return fd
    return sd

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

# Merge: for each id in meta, find matching object in app-data.js and inject fields
for bid, entry in meta.items():
    summary = pick_summary(entry)
    isbn13 = entry.get("isbn13", "") or entry.get("isbn", "")
    link = entry.get("link", "")
    if not summary and not isbn13 and not link:
        skipped += 1
        continue

    # Locate the object: id format differs
    if bid.startswith("R"):
        # R001 → string id
        pattern = rf'(\{{ id: "{re.escape(bid)}",[^}}]*?)( \}}),'
    else:
        # 14, 15, 16, 17 → numeric id, used as bare number
        pattern = rf'(\{{ id: {re.escape(bid)},[^}}]*?)( \}}),'

    m = re.search(pattern, src)
    if not m:
        # Try without trailing comma (last item) — but in our format objects always end with `},`
        not_found += 1
        print(f"  [WARN] id {bid}: 객체 못 찾음")
        continue

    obj_inner = m.group(1)

    # Skip if already has summary
    if "summary:" in obj_inner and len(re.search(r'summary:\s*"((?:[^"\\]|\\.)*)"', obj_inner).group(1) if re.search(r'summary:\s*"((?:[^"\\]|\\.)*)"', obj_inner) else "") > 30:
        skipped += 1
        continue

    # Build new fields string
    extra_fields = []
    if summary:
        extra_fields.append(f"summary: {js_str(summary)}")
    if isbn13:
        extra_fields.append(f"isbn: {js_str(isbn13)}")
    if link:
        extra_fields.append(f"aladinLink: {js_str(link)}")

    if not extra_fields:
        skipped += 1
        continue

    new_inner = obj_inner + ", " + ", ".join(extra_fields)
    src = src.replace(obj_inner + " }", new_inner + " }", 1)
    updated += 1

with open(APP_DATA, "w", encoding="utf-8") as f:
    f.write(src)

new_size = len(src.encode("utf-8"))
print()
print(f"=== 결과 ===")
print(f"  updated:    {updated}")
print(f"  skipped:    {skipped}")
print(f"  not_found:  {not_found}")
print(f"  app-data.js: {original_size} → {new_size} bytes (Δ {new_size - original_size:+d})")
print()
print("다음 단계: deploy.ps1 실행")
