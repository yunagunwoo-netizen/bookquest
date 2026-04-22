# BookQuest Changelog

## 2026-04-23
- UI 아이콘 v1 시스템 도입: `icons/v1/` 57종 PNG + `Icon` 컴포넌트 + 55종 이모지 fallback, 1순위 9곳(스트릭 카드 동적·배틀 라운드/최종·Q&A 정오답) 적용. 폴더명 소문자 정상화(V1→v1), index.html 꼬리 16 KB truncation 복구.
- (Session #2) 상점 🔓히든 탭 렌더링 분기 추가 — 히든 12종 코인 구매 경로 완전 차단, 해금 조건 힌트 + 진행도 바(N/target) + 🔒잠김/🔓해금 상태 배지. Edit 도구 꼬리 truncation 재발 → python 바이트 치환으로 우회 후 복구.

## 2026-04-22
- 히든 해금 시스템 `HIDDEN_UNLOCK_RULES` 12종 구현(한국영웅 2 + 포켓몬 5 + 히든 브롤 5) + 🔓히든 탭/진행률 카드. storeHidden 정책(오리지널 10·HOF 30 = 진열, 나머지 106 = 숨김) 확정. 탭 카운터 matchTier 기준으로 수정. sejong/arthur/zeus 주석 버그 복원(143→146).

## 그 이전
- 2026-04-22 초기: V3.4 Hall of Fame 37종 + V3.5 치비 아이콘 32종 듀얼 에셋, 오리지널 동물 10종 무료화, 브롤스타즈 99종 상점 숨김 정책 도입.
