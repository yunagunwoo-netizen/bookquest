# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29 (밤) — Phase B 전체 완료

---

## 이번 세션에서 완료한 작업 (오늘 한 줄 요약)

**Layer 1.5 Phase B 전체 완료** — CURRICULUM_BOOKS 54권 모두 25/25/8 풀 확장. 풀 콘텐츠 ~2,400 항목 추가. React #310 잠재 버그 근본 수정. CurriculumScreen 데이터 모델을 책 중심으로 전환. 홈 카드 grid 3분할.

### 1. Layer 1.5 Phase B Round 1 — 초1 5권 (C026~C030)
- 무지개 물고기·구름빵·알사탕·책 먹는 여우·점
- 235 항목 추가 / C029 "절망"→"슬퍼하기" 자동 교정

### 2. React error #310 근본 수정
- CurriculumScreen()을 conditional 렌더 안에서 함수 호출하던 패턴이 hook count 미스매치 유발
- ProfileSetupScreen이 가지고 있던 사전 호출 패턴 적용 (`const curriculumContent = CurriculumScreen();`)
- 새 Screen 추가 시 반드시 같은 패턴 사용 (메인 렌더링 직전 사전 호출)

### 3. CurriculumScreen 데이터 모델 전환 (단원→책 → 책→단원 태그)
- 학년별 책 6권 카드 + 카드마다 학기·단원 태그
- 데이터 소스: CURRICULUM_BOOKS[].curriculumLinks 직접 활용
- 빈 단원 자동 안 보임 / 중복 책 자연스럽게 표시

### 4. 백로그 #002 등록
- 교과 연계 도서 학년별 6권 → 12권 확장 (장기 과제)

### 5. Layer 1.5 Phase B Round 2 — 초2 6권 (C031~C036)
- 만복이네 떡집·나쁜 어린이표·수박 수영장·잘못 뽑은 반장·종이 봉지 공주·전천당
- 282 항목 추가 / C035 "본질"·"비극적" 자동 교정

### 6. 홈 화면 교과 연계 카드 grid 3분할
- `display: flex, overflowX: auto` → `grid, gridTemplateColumns: repeat(3, 1fr)`
- 3권 한 화면, 좌우 스크롤 제거

### 7. Layer 1.5 Phase B Round 3~9 — 초3~중3 7학년 40권 일괄 확장
- 초3 (C037~C042) / 초4 (C002·C003·C013·C014·C015) / 초5 (C004·C005·C006·C016·C017·C018)
- 초6 (C007·C008·C009·C019·C020·C021) / 중1 (C010·C011·C012·C022·C023·C024)
- 중2 (C043~C048) / 중3 (C050~C054)
- **약 1,888 항목 일괄 추가** (한 commit으로 push)

---

## 핵심 인프라

### `app.html` 유틸 함수 (이전 세션 도입, 그대로 사용 중)
```js
const ALLOWED_LEVELS = { "1": ["easy"], ..., "중3": ["hard","expert"] };
const filterByLevel = (items, userGrade) => { ... };
const stableHash = (text) => { ... };
const prioritizeByUsedSet = (items, getKey, usedSetMap, seed) => { ... };
```

### state (Firestore 백업 포함)
- quizSeenMap, discussionSeenMap, deepSeenMap — used-set
- quizShuffleSeed, discussionShuffleSeed, deepShuffleSeed — 셔플 안정화

### 이번 세션 신규 패턴
- **사전 호출 패턴 (React #310 회피)** — 새 Screen 컴포넌트가 hook 사용하면 반드시 메인 렌더링 직전 `const xxxContent = XScreen();` 사전 호출 후 conditional 렌더에서 변수 참조
- **CurriculumScreen 새 데이터 모델** — `CURRICULUM_BOOKS[].curriculumLinks`를 책 중심으로 역매핑
- **홈 카드 grid 3분할** — overflowX flex 대신 grid 3 columns로 한 화면 균등 분할

---

## 다음 세션 시작 시 이어서 할 일 (우선순위)

### 즉시 할 일
1. **deprecated meta 태그 fix** (1분)
   - `<meta name="apple-mobile-web-app-capable">` 외에 `<meta name="mobile-web-app-capable">` 추가
   - 콘솔 경고 1개 정리

2. **시즌 도서 풀 확장** (선택)
   - SEASON1_BOOKS 13권 / SEASON2_BOOKS 48권
   - 시즌2 도서는 `level` 태그 적용 필수 (난이도 필터용)
   - level 태그 없으면 기존처럼 모든 학년 노출

### [수동 — 사용자가 직접]
3. **표지 이미지 수집 — 78권** (`BookQuest_표지수집목록.docx` 활용)
4. **UI 아이콘 재크롭 + 배경 투명화**
5. **배틀 아바타 공격 컷신 이미지 생성** (나노바나나)

### 장기 과제
- **백로그 #002 — 교과 연계 도서 학년별 6권 → 12권 확장** (Phase B 끝남, 다음 큰 단계)
- Layer 2 — 응답시간 모니터링 + 챕터별 시퀀스 (진짜 독서 검증)
- Layer 3 — Spaced Repetition (망각곡선)
- 콘텐츠 풀이 더 커지면 → app.html에서 책 콘텐츠 별도 JSON 분리 (Babel 500KB 경고 대응)
- 시즌3 도서 큐레이션 (16주 신규 16권)
- 출판사 파트너십 / 교육청 연계

---

## 작업 가이드 문서 (outputs/)

- phaseB_grade1_pools.py — 초1 5권 풀 (235 항목)
- phaseB_grade1_splice.py — 풀 binary splice 표준 스크립트
- phaseB_grade2_pools.py — 초2 6권 풀 (282 항목)
- phaseB_grade3_pools.py — 초3 6권 풀 (282 항목)
- phaseB_grade4_pools.py — 초4 5권 풀 (235 항목)
- phaseB_grade5_pools.py — 초5 6권 풀 (282 항목)
- phaseB_grade6_pools.py — 초6 6권 풀 (282 항목)
- phaseB_grade_m1_pools.py — 중1 6권 풀 (282 항목)
- phaseB_grade_m2_pools.py — 중2 6권 풀 (282 항목)
- phaseB_grade_m3_pools.py — 중3 5권 풀 (235 항목)

→ 새 풀 라운드 시작 시 위 패턴 그대로 복제. splice 스크립트 그대로 재사용.

---

## 데이터 현황

| 항목 | 권수 / 사이즈 |
|---|---|
| CURRICULUM_BOOKS | **54권 모두 25/25/8 이상 도달** (Phase B 전체 완료) |
| SEASON1_BOOKS | 13권 (5/5/3, 풀 확장 대기) |
| SEASON2_BOOKS | 48권 (5/5/3, 풀 확장 대기) |
| C001 마당을 나온 암탉 | 25/25/15 (Phase A) |
| C049 데미안 | 25/25/15 (Phase A) |
| 그 외 52권 (C002~C048, C050~C054) | 25/25/8 (Phase B Round 1~9) |
| CURRICULUM_MAP 학년 | 9개 (1·2·3·4·5·6·중1·중2·중3) |
| FREE_BOOK_IDS | 동적 매핑 (CURRICULUM_BOOKS 모두 포함) |
| **app.html** | **~1.735 MB** (1,734,792 bytes) |
| **CurriculumScreen** | 책 중심 구조 |
| **홈 교과 연계 카드** | grid 3분할 |

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html                           # 메인 앱 (단일 파일 React PWA, ~1.735 MB)
├── index.html                         # 랜딩 페이지
├── sw.js                              # Service Worker
├── manifest.json                      # PWA 매니페스트
├── firestore.rules                    # Firestore 보안 규칙
├── firebase.json
├── .nojekyll                          # GitHub Pages Jekyll 비활성화
├── deploy.ps1                         # 배포 자동화 + sanity check
├── 아이디어_백로그.md                 # #001 유튜브 숏츠, #002 도서 12권 확장
├── BookQuest_표지수집목록.docx
├── icons/
└── skills/
    └── bookquest-season-builder/SKILL.md
```

---

## 주요 코드 위치 (app.html)

| 구조 | 위치 |
|---|---|
| ALLOWED_LEVELS / filterByLevel | computeAvatarStats 직전 |
| stableHash / prioritizeByUsedSet | 같은 영역 |
| CURRICULUM_MAP (9개 학년) | ~682줄 |
| CURRICULUM_BOOKS C001~C054 | ~830줄~ |
| 책 상세 토론/퀴즈/심화 탭 | bookTab === "discuss"/"quiz"/"deep" IIFE |
| **CurriculumScreen (책 중심)** | ~15083줄 |
| **사전 호출 패턴 (#310 회피)** | ~15599줄 메인 렌더링 직전 |
| **홈 교과 연계 grid 3분할** | ~14586줄 |

---

## 배포 명령어

```powershell
cd C:\dev\bookquest
.\deploy.ps1 "feat: 어떤 변경"
```

Sanity check 단계가 OK여야 push 진행. 빨간 XX는 push 중단.

---

## 주의사항 / 알려진 이슈

- **app.html이 ~1.735 MB로 커짐** — Edit tool 끝부분 truncation / NULL 패딩 위험 매우 큼
  - 대량·소량 변경 모두 Python binary mode 처리 권장
  - deploy.ps1 sanity check가 1차 가드 (size + </html> + no NULL padding)
  - NULL 패딩 발견 시 Python으로 `.rstrip(b'\x00')` 후 다시 write
  - Edit이 truncation 일으키면 git checkout으로 복원 → Python으로 재적용
- **새 Screen 컴포넌트 추가 시** — hook 사용하면 반드시 사전 호출 패턴. 직접 함수 호출하면 React error #310 위험
- **한글 파일명 OK** (.nojekyll 덕분)
- **Cowork sandbox는 git 작업 권한 제한** — `.git\index.lock` 잔재 deploy.ps1이 자동 정리
- **Babel script 500KB 초과 경고** — 동작 영향 없음, 1.7MB 도달로 콘텐츠 JSON 분리 필요성 점점 커짐
- **`apple-mobile-web-app-capable` deprecated 경고** — 동작 영향 없음, 1줄 fix 가능 (다음 세션 즉시 처리)

---

## 풀 검수 체크리스트 (다음 라운드용)

splice 후 확인:
1. </html> 종료 + NULL 패딩 없음
2. 책 객체 {} [] 균형 OK
3. 책 객체 단독 JS literal node --check 통과
4. 풀 카운트 (≥25/25/8) 모두 ✓
5. choice 퀴즈 answer 인덱스가 options 범위 안
6. 학년별 부적합 어휘 grep:
   - **초저학년 (1·2·3)**: 본질·정체성·비극적·절망·우울·윤리적·천착·대두·보편적
   - **초고학년 (4·5·6)**: 좀 더 관대 — 추상명사 일부 허용
   - **중학생 (중1~3)**: 추상 개념 허용 (C049 데미안 패턴 참고)
7. 원본 데이터(summary, keyPoints)에 이미 있는 단어는 화이트리스트로 보존

---

## Git 커밋 히스토리 (이번 세션)

| commit | 메시지 |
|---|---|
| 564cdbc | feat: Phase B Round 1 초1 5권 (revert됨) |
| ab168d5 | revert: CurriculumScreen 빈 화면 에러 |
| 5278378 | fix: CurriculumScreen React error #310 사전 호출 |
| 7d398aa | feat: Phase B Round 1 초1 5권 재투입 |
| 1d65c42 | feat: 교과연계 책 중심 구조 전환 + 백로그 #002 |
| ca35073 | feat: Phase B Round 2 초2 6권 |
| 4f62bfb | feat: 홈 교과 연계 grid 3분할 + 핸드오프 정리 |
| **799a8fb** | **feat: Phase B Round 3~9 초3~중3 7학년 40권 일괄 확장** |

---

## 이전 세션 누적 핵심 (보존)

### Layer 1 — 출제 풀 셔플 + used-set
- 부분 표시: 토론 5→3, 퀴즈 5→4, 심화 3→2
- 셔플 우선순위: 안 본 항목 → 오래 본 항목 → 최근 본 항목
- 🔄 다른 주제 보기 버튼
- used-set Firestore 백업

### 학년별 난이도 필터
- ALLOWED_LEVELS / filterByLevel
- level 없는 항목은 모든 학년 노출

### 프로필 학년 9개 통일 + 빠른 학년 변경 위젯 (관리자 전용)

### 배포 자동화 — deploy.ps1
- 잔재 정리 / SW 캐시 bump / sanity check / git push
- UTF-8 BOM (한글 메시지 안전)

### 버그 수정 (이전)
- SW 외부 origin 통과
- Firestore 보안 규칙
- app.html truncation 가드
