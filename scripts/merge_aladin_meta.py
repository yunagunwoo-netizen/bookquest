#!/usr/bin/env python3
"""
scripts/merge_aladin_meta.py - v2 (brace-balanced parser)

Merge aladin_meta.json into RECOMMENDED_BOOKS / EXTRA_BOOKS objects in app-data.js.
Inject summary, isbn, aladinLink fields.

v1 used regex which mismatched on certain summary characters and could damage the
file. v2 uses balanced brace counters to slice each object exactly. Safe.

Usage:
    cd C:\\dev\\bookquest
    python scripts/merge_aladin_meta.py

Prereq:
    - scripts/fetch_aladin_descriptions.js executed first
    - ocr_results/aladin_meta.json exists

Safety:
    - automatic backup of app-data.js into backup/ before editing
    - per-object processing, no partial-corruption risk
    - summary picks the longer of fullDescription / description
    - skip if existing summary > 30 chars (resume support)
"""

import json
import re
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_DATA = ROOT / "app-data.js"
META_PATH = ROOT / "ocr_results" / "aladin_meta.json"
BACKUP_DIR = ROOT / "backup"

if not META_PATH.exists():
    print("[ERR] " + str(META_PATH) + " not found.")
    print("      Run scripts/fetch_aladin_descriptions.js first.")
    exit(1)

if not APP_DATA.exists():
    print("[ERR] " + str(APP_DATA) + " not found.")
    exit(1)

BACKUP_DIR.mkdir(exist_ok=True)
ts = time.strftime("%Y%m%d_%H%M%S")
bk = BACKUP_DIR / ("app-data-pre-merge-" + ts + ".js")
shutil.copy(APP_DATA, bk)
print("[OK] backup: " + bk.name)

with open(META_PATH, encoding="utf-8") as f:
    meta = json.load(f)
print("[OK] aladin_meta entries: " + str(len(meta)))

with open(APP_DATA, encoding="utf-8") as f:
    src = f.read()

original_size = len(src.encode("utf-8"))


def slice_array(text, name):
    """Return (start, end+1) of the [...] block for `const NAME = [...]`."""
    m = re.search(r"const " + re.escape(name) + r"\s*=\s*\[", text)
    if not m:
        return None, None
    start = m.end() - 1
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return start, i + 1
    return start, None


def split_objects(arr_text):
    """Return (start, end) ranges of top-level { ... } objects inside [ ... ]."""
    inside = arr_text[1:-1]
    objs = []
    depth, in_str, esc = 0, False, False
    obj_start = None
    for i, c in enumerate(inside):
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and obj_start is not None:
                # +1 to compensate for the leading '[' in arr_text
                objs.append((obj_start + 1, i + 2))
                obj_start = None
    return objs


def get_obj_id(obj_text):
    m = re.search(r'\bid:\s*(?:"([^"]+)"|(\d+))', obj_text)
    if not m:
        return None
    return m.group(1) or m.group(2)


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def pick_summary(entry):
    fd = (entry.get("fullDescription") or "").strip()
    sd = (entry.get("description") or "").strip()
    return fd if len(fd) >= max(50, len(sd)) else sd


def build_new_array(arr_text, objs, prefix="  "):
    new_objs, updated, skipped = [], 0, 0
    for s, e in objs:
        obj_text = arr_text[s:e]
        bid = get_obj_id(obj_text)
        if bid not in meta:
            new_objs.append(obj_text)
            skipped += 1
            continue
        entry = meta[bid]
        summary = pick_summary(entry)
        isbn = entry.get("isbn13", "") or entry.get("isbn", "")
        link = entry.get("link", "")

        existing = re.search(r'summary:\s*"((?:[^"\\]|\\.)*)"', obj_text)
        if existing and len(existing.group(1)) > 30:
            new_objs.append(obj_text)
            skipped += 1
            continue

        parts = []
        if summary:
            parts.append("summary: " + js_str(summary))
        if isbn:
            parts.append("isbn: " + js_str(isbn))
        if link:
            parts.append("aladinLink: " + js_str(link))
        if not parts:
            new_objs.append(obj_text)
            skipped += 1
            continue

        last_brace = obj_text.rfind("}")
        before = obj_text[:last_brace].rstrip()
        if before.endswith(","):
            before = before[:-1]
        new_objs.append(before + ", " + ", ".join(parts) + " }")
        updated += 1

    new_arr = "[\n" + ",\n".join(prefix + o for o in new_objs) + "\n]"
    return new_arr, updated, skipped


totals = {"updated": 0, "skipped": 0}
for arr_name in ["RECOMMENDED_BOOKS", "EXTRA_BOOKS"]:
    s, e = slice_array(src, arr_name)
    if s is None:
        print("[WARN] " + arr_name + " not found - skipping")
        continue
    arr_text = src[s:e]
    objs = split_objects(arr_text)
    print("[OK] " + arr_name + ": " + str(len(objs)) + " objects")
    new_arr, upd, skp = build_new_array(arr_text, objs)
    src = src[:s] + new_arr + src[e:]
    totals["updated"] += upd
    totals["skipped"] += skp
    print("     " + arr_name + ": " + str(upd) + " updated / " + str(skp) + " skipped")

with open(APP_DATA, "w", encoding="utf-8") as f:
    f.write(src)

new_size = len(src.encode("utf-8"))
delta = new_size - original_size
sign = "+" if delta >= 0 else ""

print()
print("=== Result ===")
print("  updated total: " + str(totals["updated"]))
print("  skipped total: " + str(totals["skipped"]))
print("  app-data.js: " + str(original_size) + " -> " + str(new_size) + " bytes (delta " + sign + str(delta) + ")")
print()
print("Next: .\\deploy.ps1")
