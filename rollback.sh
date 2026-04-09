#!/bin/bash
# BookQuest 캐릭터 롤백 스크립트
# 오리지널 캐릭터 ↔ 브롤스타즈 캐릭터 전환
#
# 사용법:
#   ./rollback.sh brawl    → 브롤스타즈 캐릭터로 전환 (롤백)
#   ./rollback.sh original → 오리지널 캐릭터로 전환
#   ./rollback.sh status   → 현재 상태 확인

DIR="$(cd "$(dirname "$0")" && pwd)"

check_status() {
  if grep -q '"lumi"' "$DIR/index.html" 2>/dev/null; then
    echo "🦊 현재: 오리지널 캐릭터 (루미/미오/노아)"
    return 0  # original
  else
    echo "🎮 현재: 브롤스타즈 캐릭터 (칼/콜레트/바이런)"
    return 1  # brawl
  fi
}

case "$1" in
  brawl|rollback)
    if ! grep -q '"lumi"' "$DIR/index.html" 2>/dev/null; then
      echo "이미 브롤스타즈 캐릭터입니다."
      exit 0
    fi
    if [ ! -f "$DIR/index_brawlstars_backup.html" ]; then
      echo "❌ 백업 파일이 없습니다: index_brawlstars_backup.html"
      exit 1
    fi
    # 현재 오리지널 버전 백업
    cp "$DIR/index.html" "$DIR/index_original_backup.html"
    cp "$DIR/functions/index.js" "$DIR/functions/index_original_backup.js"
    # 브롤스타즈 버전으로 복원
    cp "$DIR/index_brawlstars_backup.html" "$DIR/index.html"
    cp "$DIR/functions/index_brawlstars_backup.js" "$DIR/functions/index.js"
    echo "✅ 브롤스타즈 캐릭터로 롤백 완료!"
    echo "   firebase deploy를 다시 실행하세요."
    ;;

  original)
    if grep -q '"lumi"' "$DIR/index.html" 2>/dev/null; then
      echo "이미 오리지널 캐릭터입니다."
      exit 0
    fi
    if [ ! -f "$DIR/index_original_backup.html" ]; then
      echo "❌ 백업 파일이 없습니다: index_original_backup.html"
      exit 1
    fi
    cp "$DIR/index_original_backup.html" "$DIR/index.html"
    cp "$DIR/functions/index_original_backup.js" "$DIR/functions/index.js"
    echo "✅ 오리지널 캐릭터로 전환 완료!"
    echo "   firebase deploy를 다시 실행하세요."
    ;;

  status)
    check_status
    echo ""
    echo "📁 백업 파일 상태:"
    [ -f "$DIR/index_brawlstars_backup.html" ] && echo "  ✓ index_brawlstars_backup.html" || echo "  ✗ index_brawlstars_backup.html (없음)"
    [ -f "$DIR/index_original_backup.html" ] && echo "  ✓ index_original_backup.html" || echo "  ✗ index_original_backup.html (없음)"
    [ -f "$DIR/functions/index_brawlstars_backup.js" ] && echo "  ✓ functions/index_brawlstars_backup.js" || echo "  ✗ functions/index_brawlstars_backup.js (없음)"
    [ -f "$DIR/functions/index_original_backup.js" ] && echo "  ✓ functions/index_original_backup.js" || echo "  ✗ functions/index_original_backup.js (없음)"
    ;;

  *)
    echo "BookQuest 캐릭터 전환 스크립트"
    echo ""
    echo "사용법:"
    echo "  ./rollback.sh brawl    → 브롤스타즈 캐릭터로 롤백"
    echo "  ./rollback.sh original → 오리지널 캐릭터로 전환"
    echo "  ./rollback.sh status   → 현재 상태 확인"
    echo ""
    check_status
    ;;
esac
