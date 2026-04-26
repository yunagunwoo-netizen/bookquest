# BookQuest Changelog

## 2026-04-25
- UI 아이콘 4종 크기 24×24px 고정 + flexbox 정렬. 배틀 직접참여 50코인/2회로 변경. 장영실·유관순 heroic(800) 이동. 홈 화면 배지 섹션 제거. Enchanted Abyss 다크 스킨 적용 후 롤백(revert e2f3740). 총 156종 / 진열 42 / 숨김 114.
- (Session 2) 배틀 카드 포켓몬카드 스타일 리디자인: BattleCard(152px) + ResultCard(130px) — 타입아이콘/이름/HP, 아바타+Lv뱃지+레어리티뱃지, 칭호, 기술2개(레어리티별), HP바+타입라벨, 샤인 오버레이. CARD_TYPE/CARD_SKILL 상수 추가. RARITY_BADGE_STYLE·RARITY_LABEL에 heroic/mythic/hidden 확장. 카드 이미지 52종(600x840 PNG) Pillow 합성 + cardImg 필드 주입. AI HUB 아바타 랜덤 대사 24종(3단계x8개). rounds[0] 크래시 버그 수정. 책 상세 탭 flexWrap 적용.

## 2026-04-24
- 기술 부채 정리: `version.js`(iCoach 잔재, APP_VERSION β1.4.15) 삭제 + `sw.js` precache에서 제거. 레거시 `icons/tab-{home,question,explore,profile}.png` 4개 삭제(참조 0회 검증), `tab-daily.png`는 L6451 일일 미션 헤더에서 직접 참조 중이라 유지. `PNG_ICONS` 맵의 tab_* 5키 dead entry 제거(−212바이트). `icons/v1/_unused/` 폴더 3장(theme_art/global/psychology) 삭제. index.html 156종 / 숨김 116 산술 오차 저녁 핸드오프·CHANGELOG 동시 수정. Babel 재파싱 OK, `</html>` 정상 종료.

## 2026-04-23
- UI 아이콘 v1 시스템 도입: `icons/v1/` 57종 PNG + `Icon` 컴포넌트 + 55종 이모지 fallback, 1순위 9곳(스트릭 카드 동적·배틀 라운드/최종·Q&A 정오답) 적용. 폴더명 소문자 정상화(V1→v1), index.html 꼬리 16 KB truncation 복구.
- (Session #2) 상점 🔓히든 탭 렌더링 분기 추가 — 히든 12종 코인 구매 경로 완전 차단, 해금 조건 힌트 + 진행도 바(N/target) + 🔒잠김/🔓해금 상태 배지. Edit 도구 꼬리 truncation 재발 → python 바이트 치환으로 우회 후 복구.
- (저녁 세션) v1.5~v1.8 대규모 업데이트: UI 아이콘 15종 + 탭바 10종(active/inactive) + 배경 5장 + 히든 전설 10인(V3.6 오리지널 IP) + 성소의 파수꾼 테마팩 11종 Nano Banana 생성. 히든 티어 포켓몬/브롤 10종 → 책 속 전설 10인(homer/scheherazade/hypatia/merlin/confucius/socrates/cleopatra/galileo/musashi/sage_archivist)로 교체(IP 리스크 해소). 홀로그래픽 CSS 셔머 효과, BattleScreen 3단계 배경, AIHubScreen 아바타+말풍선, RankingScreen 명예의 전당 히어로, TabBar 프리미엄 다크 판타지 전환. PWA 배포 인프라(sw.js 재작성 + `bq-deploy` + `-v` NEXT_RELEASE.md 자동 CHANGELOG/APP_VERSION 주입 + truncation safety guard + SW 자동 리로드) 구축. 사업계획서 v2 개정판 + PPT 18슬라이드 생성. AVATAR_DATA 총 156종(_av 109 + _av34 37 + _av36 10), 진열 40 / 숨김 116.

## 2026-04-22
- 히든 해금 시스템 `HIDDEN_UNLOCK_RULES` 12종 구현(한국영웅 2 + 포켓몬 5 + 히든 브롤 5) + 🔓히든 탭/진행률 카드. storeHidden 정책(오리지널 10·HOF 30 = 진열, 나머지 106 = 숨김) 확정. 탭 카운터 matchTier 기준으로 수정. sejong/arthur/zeus 주석 버그 복원(143→146).

## 그 이전
- 2026-04-22 초기: V3.4 Hall of Fame 37종 + V3.5 치비 아이콘 32종 듀얼 에셋, 오리지널 동물 10종 무료화, 브롤스타즈 99종 상점 숨김 정책 도입.
