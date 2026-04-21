/**
 * iCoach 단일 버전 소스 (Single Source of Truth)
 * -----------------------------------------------
 * 앱 버전을 올릴 때는 이 파일의 상단 3개 상수만 수정하면 됩니다.
 * index.html 의 히어로 칩이 이 값을 자동으로 읽어 렌더링합니다.
 * (app.html 의 배지 / 업데이트 블록은 릴리스 노트와 함께 수동 관리 — 업데이트 문구가 버전 숫자와 한 묶음이라 그게 더 안전합니다.)
 *
 * 릴리스 체크리스트 (복붙용):
 *   1) version.js  — APP_VERSION / APP_VERSION_DATE / APP_CACHE 갱신
 *   2) sw.js       — CACHE_NAME 을 APP_CACHE 값과 일치시킴
 *   3) app.html    — 버전 배지 및 업데이트 블록 수정 (디자인/문구 수동 관리)
 *   4) PROJECT_STATUS.md / RELEASE_NOTES_*.md 갱신
 *
 * 자동 반영되는 항목 (이 파일만 고치면 같이 바뀜):
 *   • index.html 히어로 칩 (id="version-chip")
 *   • app.html 의 const APP_VERSION → 버전별 롤백 리스트 라벨("β x.y")
 */

// ── 한 곳만 고치세요 ──────────────────────────────────
window.APP_VERSION      = 'β 1.4.15';        // 히어로 칩에 노출됨
window.APP_VERSION_DATE = '2026.04.21';      // 릴리스 일자 (YYYY.MM.DD)
window.APP_CACHE        = 'icoach-v155';     // sw.js 의 CACHE_NAME 과 일치해야 함
// ─────────────────────────────────────────────────────

// 랜딩 칩에 자동 주입 (id="version-chip" 를 가진 요소를 찾아 텍스트 갱신)
(function renderVersionChip(){
  function apply(){
    var el = document.getElementById('version-chip');
    if(!el) return;
    var label = (window.APP_VERSION || '').trim();
    if(!label) return;
    // 칩 안의 도트(.dot) 스팬은 유지하고, 그 뒤 텍스트만 교체
    var textNode = null;
    for(var i=0;i<el.childNodes.length;i++){
      var n = el.childNodes[i];
      if(n.nodeType === 3 /* TEXT_NODE */){ textNode = n; break; }
    }
    var newText = ' ' + label + ' 테스트 중';
    if(textNode){ textNode.nodeValue = newText; }
    else { el.appendChild(document.createTextNode(newText)); }
    el.setAttribute('title', label + ' · ' + (window.APP_VERSION_DATE || '') + ' · ' + (window.APP_CACHE || ''));
  }
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
