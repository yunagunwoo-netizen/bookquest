# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29

---

## 이번 세션에서 완료한 작업

### 1. Layer 1 — 출제 풀 셔플 + used-set
책 상세 화면(토론·퀴즈·심화 탭)에서 매번 다른 셋이 노출되도록 인프라 구축.
- **부분 표시**: 토론 5→3, 퀴즈 5→4, 심화 3→2 (저학년은 심화 풀 자체가 작음)
- **셔플 우선순위**: 안 본 항목 → 오래 본 항목 → 최근 본 항목
- **"🔄 다른 주제 보기" 버튼** — 능동적 셋 회전
- **used-set Firestore 백업** — `quizSeenMap` / `discussionSeenMap` / `deepSeenMap`
- **셔플 시드 자동 새로고침** — 책 진입할 때마다

### 2. Layer 1.5 Phase A — 학년별 톤 차등 + 풀 25개 확장 (3권 테스트)
- **C001 마당을 나온 암탉** (초4) — 퀴즈 25 / 토론 25 / 심화 15
- **C025 강아지똥** (초1) — 퀴즈 25 / 토론 25 / 심화 8 (저학년 심화 풀 작음)
- **C049 데미안** (중3) — 퀴즈 25 / 토론 25 / 심화 15

### 3. 학년별 난이도 필터 — 시즌 도서용
- `ALLOWED_LEVELS` 상수 — 학년별 허용 난이도 (`easy`/`medium`/`hard`/`expert`)
- `filterByLevel(items, userGrade)` — `level` 태그 있으면 학년에 맞는 것만 노출
- 토론·퀴즈·심화 탭 모두 적용. **`level` 없는 항목은 모든 학년 노출** (교과 연계 호환)
- 시즌 도서는 차후 콘텐츠 작성 시 `level` 태그 추가 필요

### 4. 프로필 학년 옵션 확장
- **3곳** 학년 선택 UI 모두 9개 학년으로 통일
- 학년 라벨 `초1·초2·초3·초4·초5·초6·중1·중2·중3` 표시

### 5. 빠른 학년 변경 위젯 → 관리자 전용
- 일반 사용자는 "프로필 수정" 화면에서만 학년 변경
- 관리자는 메인 화면에 노란 "관리자" 배지와 함께 빠른 변경 카드 노출

### 6. 배포 자동화 — `deploy.ps1`
```
.\deploy.ps1 "커밋 메시지"
```
- 잔재 정리 (`.git\index.lock`, `*.bak`)
- SW 캐시 버전 자동 bump
- **app.html sanity check** — 사이즈 / `</html>` 종료 / NULL 패딩 3중 검증
- git add → commit → push
- UTF-8 BOM 적용으로 한글 메시지 안전

### 7. 버그 수정
- **SW 외부 origin 통과** — Firestore Listen 스트림 충돌 해결
- **Firestore 보안 규칙 파일** (`firestore.rules`) — 자동 백업 권한 거부 해결
- **app.html truncation 복구** — 안정 커밋(`0669163`)에서 변경분 재적용
- **deploy.ps1 sanity check** — 같은 truncation이 다시 GitHub에 push되지 않도록 가드

---

## 핵심 인프라 (이번 세션 신규)

### `app.html` 새 유틸 함수
```js
const ALLOWED_LEVELS = { "1": ["easy"], ..., "중3": ["hard","expert"] };
const filterByLevel = (items, userGrade) => { ... };
const stableHash = (text) => { ... };
const prioritizeByUsedSet = (items, getKey, usedSetMap, seed) => { ... };
```

### 새 state (Firestore 백업 포함)
- `quizSeenMap`, `discussionSeenMap`, `deepSeenMap` — used-set
- `quizShuffleSeed`, `discussionShuffleSeed`, `deepShuffleSeed` — 셔플 안정화

### 새 파일
- `firestore.rules` — Firestore 보안 규칙
- `deploy.ps1` — 배포 자동화 스크립트 (UTF-8 BOM)
- `.nojekyll` — GitHub Pages Jekyll 비활성화 (이전 세션)

---

## 다음 세션 시작 시 이어서 할 일 (우선순위)

### 즉시 할 일
1. **Layer 1.5 Phase B — 전체 115권 풀 25개 확장**
   - 학년 묶음 단위로 진행 (초1~중3 학년별 6권씩 → 시즌2 lower/upper/middle 16권씩)
   - **시즌 도서는 `level` 태그 적용 필수** (`grade_level_guide.md` 기준 분포)
   - 라운드마다 자동 검수 (저학년 금지 단어 grep) + 사용자 샘플 스팟체크
   - C001/C025/C049가 이미 25개로 확장되어 있으므로 그 패턴 그대로

2. **deprecated meta 태그 fix** (1분)
   - `<meta name="apple-mobile-web-app-capable">` 외에 `<meta name="mobile-web-app-capable">` 같이 추가
   - 콘솔 경고 1개 정리

### [수동 — 사용자가 직접]
3. **표지 이미지 수집 — 78권** (`BookQuest_표지수집목록.docx` 활용)
4. **UI 아이콘 재크롭 + 배경 투명화**
5. **배틀 아바타 공격 컷신 이미지 생성** (나노바나나)

### 장기 과제
- Layer 2 — 응답시간 모니터링 + 챕터별 시퀀스 (진짜 독서 검증)
- Layer 3 — Spaced Repetition (망각곡선)
- 콘텐츠 풀을 50+로 키우려면 → app.html에서 책 콘텐츠 별도 JSON 분리
- 시즌3 도서 큐레이션 (16주 신규 16권)
- 출판사 파트너십 / 교육청 연계

---

## 작업 가이드 문서 (outputs/)

- `grade_level_guide.md` — Phase B 표준 (학년군별 어휘·풀 분포·`level` 태그 정책)
- `c001_pool_additions.js`, `c001_pool_revision.js` — 초4 톤 샘플
- `c025_pool_additions.js` — 초1 톤 샘플
- `c049_pool_additions.js` — 중3 톤 샘플

→ Phase B 시작 시 이 가이드를 그대로 적용하면 됨.

---

## 데이터 현황

| 항목 | 권수 / 사이즈 |
|---|---|
| CURRICULUM_BOOKS | 54권 (C001~C054) |
| SEASON1_BOOKS | 13권 |
| SEASON2_BOOKS | 48권 (lower 16 / upper 16 / middle 16) |
| **C001/C025/C049 풀** | **25/25/15(or 8) 확장 완료** |
| 나머지 112권 풀 | 5/5/3 (Phase B 대기) |
| CURRICULUM_MAP 학년 | 9개 (1·2·3·4·5·6·중1·중2·중3) |
| FREE_BOOK_IDS | 동적 매핑 (CURRICULUM_BOOKS 모두 포함) |
| app.html | ~963 K characters (~1.25 MB) |
| 학년 필터 | `ALLOWED_LEVELS` + `filterByLevel` 적용 |

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html                           # 메인 앱 (단일 파일 React PWA, ~1.25 MB)
├── index.html                         # 랜딩 페이지
├── sw.js                              # Service Worker (외부 origin 통과 fix 적용)
├── manifest.json                      # PWA 매니페스트
├── firestore.rules                    # Firestore 보안 규칙 (신규)
├── firebase.json                      # firestore 섹션 추가됨
├── .nojekyll                          # GitHub Pages Jekyll 비활성화
├── deploy.ps1                         # 배포 자동화 + sanity check (UTF-8 BOM)
├── BookQuest_표지수집목록.docx        # 78권 표지 수집 가이드
├── icons/
├── skills/
│   └── bookquest-season-builder/SKILL.md
└── 앱스크린샷_*.jpg
```

---

## 주요 코드 위치 (app.html)

| 구조 | 위치 |
|---|---|
| ALLOWED_LEVELS / filterByLevel | computeAvatarStats 직전 |
| stableHash / prioritizeByUsedSet | 같은 영역 |
| SEASONS / CURRENT_SEASON | ~661줄 |
| GRADE_TO_TIER / getTier | ~672줄 |
| CURRICULUM_MAP (9개 학년) | ~682줄 |
| CURRICULUM_BOOKS C001~C054 | ~830줄~ |
| SEASON2_BOOKS (level 태그 미적용) | grep으로 위치 확인 |
| 책 상세 토론/퀴즈/심화 탭 | `bookTab === "discuss"` / `"quiz"` / `"deep"` IIFE |
| 빠른 학년 변경 위젯 (isAdmin 전용) | `{isAdmin && (` 검색 |

---

## 배포 명령어 (PowerShell)

```powershell
cd C:\dev\bookquest
.\deploy.ps1 "feat: 어떤 변경"
```

> 처음 한 번 막히면: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

`Sanity-check app.html` 단계가 OK로 떠야 push가 진행됨. 빨간 XX가 뜨면 push 중단되니 sandbox에서 파일을 다시 확인할 것.

---

## 주의사항 / 알려진 이슈

- **app.html이 ~1.25 MB로 커짐** — Edit tool로 수정 시 끝부분이 잘리는(truncation) 사례가 있음
  - 대량 변경은 Python splice 스크립트로 binary 모드 쓰기 (NULL 패딩 / 끝 종료 검증 포함)
  - deploy.ps1의 sanity check가 1차 가드 역할
- **한글 파일명 OK** (`.nojekyll` 덕분에 GitHub Pages Jekyll 안 거침)
- **Cowork sandbox는 git 작업 권한 제한** — `.git\index.lock` 잔재 생기면 deploy.ps1이 자동 정리
- **Babel script 500KB 초과 경고** — 콘솔에 뜨지만 동작에 영향 없음 (장기적으론 콘텐츠 JSON 분리 필요)
- **`apple-mobile-web-app-capable` deprecated 경고** — 동작 영향 없음, 1줄 fix 가능

---

## Git 커밋 히스토리 (이번 세션)

| 메시지 |
|---|
| feat: 빠른 학년 변경 위젯 관리자 전용 + 학년 라벨 초1·초2·초3 표시 |
| fix: app.html truncation 복구 + Layer 1.5 변경분 재push |
| fix: 프로필 학년 선택 옵션 9개 학년 전체로 확장 |
| feat: Layer 1.5 테스트 — 학년별 난이도 필터 + C001/C025/C049 풀 25개 확장 |
| fix: deploy.ps1 인코딩 수정 (UTF-8 BOM, 영문 메시지) |
| fix: SW 외부 origin 통과 + Firestore 보안 규칙 파일 추가 |
| feat: Layer 1 — 출제 풀 셔플 + used-set 적용 |
| feat: 시즌2 48권 책별 맞춤 콘텐츠 생성 + 중복 정리 + .nojekyll |
| feat: 교과 연계 도서 초1~중3 전학년 확장 (24→54권) |
