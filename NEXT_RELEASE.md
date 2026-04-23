# 다음 릴리스 스테이징

## 제목
chore: 기술 부채 정리 (iCoach 잔재 삭제 + 레거시 자산 제거)

## 변경
- `version.js` (iCoach 잔재 APP_VERSION β1.4.15) 삭제 — index.html 미참조
- `sw.js` precache에서 `./version.js` 제거
- `icons/tab-{home,question,explore,profile}.png` 4종 삭제 (참조 0회)
- `icons/v1/_unused/` 폴더 (theme_art/global/psychology 3장) 삭제
- `index.html` `PNG_ICONS` 맵의 tab_* dead key 5개 제거 (−212B)
- `tab-daily.png`는 일일 미션 헤더에서 직접 참조 중이라 유지
- CHANGELOG / 저녁 핸드오프의 155→156, 115→116 산술 오차 수정
