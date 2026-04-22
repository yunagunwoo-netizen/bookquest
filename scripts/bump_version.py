"""
BookQuest 버전 관리 스크립트
===============================

사용법:
  python scripts/bump_version.py --version 1.3.0 --title "제목" --changes "변경1" "변경2" "변경3"

동작:
1. 현재 index.html 읽어서 APP_VERSION 파악
2. backup/index_v{기존버전}.html 로 현재 파일 백업
3. index.html 의 APP_VERSION, APP_BUILD_DATE 갱신
4. CHANGELOG 최상단에 새 항목 추가
5. VERSION_HISTORY 에 이전 버전 항목 추가
"""
import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
BACKUP_DIR = ROOT / "backup"


def read_index():
    return INDEX.read_text(encoding="utf-8")


def write_index(content):
    INDEX.write_text(content, encoding="utf-8")


def get_current_version(content):
    m = re.search(r'const APP_VERSION = "([\d.]+)";', content)
    if not m:
        raise RuntimeError("APP_VERSION not found in index.html")
    return m.group(1)


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def make_backup(old_version):
    BACKUP_DIR.mkdir(exist_ok=True)
    dst = BACKUP_DIR / f"index_v{old_version}.html"
    shutil.copy2(INDEX, dst)
    print(f"[OK] 백업 생성: {dst.relative_to(ROOT)}")
    return dst


def bump(new_version, title, changes):
    content = read_index()
    old_version = get_current_version(content)
    today = today_str()

    if new_version == old_version:
        print(f"[WARN] 버전이 같음: {old_version}. 중단.")
        sys.exit(1)

    # 1) 백업
    make_backup(old_version)

    # 2) APP_VERSION / APP_BUILD_DATE 갱신
    content = re.sub(
        r'const APP_VERSION = "[\d.]+";',
        f'const APP_VERSION = "{new_version}";',
        content,
        count=1,
    )
    content = re.sub(
        r'const APP_BUILD_DATE = "[^"]+";',
        f'const APP_BUILD_DATE = "{today}";',
        content,
        count=1,
    )

    # 3) CHANGELOG 최상단에 삽입
    changes_js = ",\n          ".join([f'"{c}"' for c in changes])
    new_entry = (
        f'      {{\n'
        f'        version: "{new_version}",\n'
        f'        date: "{today}",\n'
        f'        title: "{title}",\n'
        f'        changes: [\n'
        f'          {changes_js}\n'
        f'        ]\n'
        f'      }},\n'
    )

    # CHANGELOG = [ 바로 다음에 삽입
    m = re.search(r'(const CHANGELOG = \[\n)', content)
    if not m:
        raise RuntimeError("CHANGELOG 배열을 찾지 못함")
    insert_pos = m.end()
    content = content[:insert_pos] + new_entry + content[insert_pos:]

    # 4) VERSION_HISTORY 업데이트 - 이전 현재버전을 이전버전으로 강등
    # "1.2.0": { file: "index.html", label: "현재 버전" } 형태를
    # backup/index_v1.2.0.html 로 바꾸고, 새 버전을 맨 위에 추가
    # 기존 "현재 버전" 항목 수정
    old_label_match = re.search(
        rf'"{old_version}": \{{ file: "index\.html", label: "현재 버전" \}},',
        content,
    )
    if old_label_match:
        # 이전 CHANGELOG 에서 old_version 의 title 가져오기
        old_title_match = re.search(
            rf'version: "{old_version}",\s+date: "[^"]+",\s+title: "([^"]+)"',
            content,
        )
        old_title = old_title_match.group(1) if old_title_match else old_version
        # 이전 current 항목을 backup 경로로 변경
        content = content.replace(
            f'"{old_version}": {{ file: "index.html", label: "현재 버전" }},',
            f'"{old_version}": {{ file: "backup/index_v{old_version}.html", label: "{old_title}" }},',
        )

    # 새 버전을 VERSION_HISTORY 최상단에 추가
    m = re.search(r'(const VERSION_HISTORY = \{\n)', content)
    if not m:
        raise RuntimeError("VERSION_HISTORY 객체를 찾지 못함")
    insert_pos = m.end()
    new_history = f'      "{new_version}": {{ file: "index.html", label: "현재 버전" }},\n'
    content = content[:insert_pos] + new_history + content[insert_pos:]

    # 5) 저장
    write_index(content)
    print(f"[OK] 버전 업데이트 완료: {old_version} -> {new_version}")
    print(f"[OK] 빌드 날짜: {today}")
    print(f"[OK] 제목: {title}")
    print(f"[OK] 변경사항 {len(changes)}개")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, help="새 버전 (예: 1.3.0)")
    parser.add_argument("--title", required=True, help="이번 버전 제목")
    parser.add_argument("--changes", required=True, nargs="+", help="변경사항 목록")
    args = parser.parse_args()

    bump(args.version, args.title, args.changes)


if __name__ == "__main__":
    main()
