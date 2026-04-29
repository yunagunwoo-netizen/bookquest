# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29 (저녁)

---

## 이번 세션에서 완료한 작업

### 1. Layer 1.5 Phase B Round 1 — 초1 5권 풀 25/25/8 확장
교과 연계 도서 초1 학년 책 6권 중 5권의 토론·퀴즈·심화 풀을 5/5/3 → 25/25/8로 확장.
- **C026 무지개 물고기** (마르쿠스 피스터)
- **C027 구름빵** (백희나)
- **C028 알사탕** (백희나)
- **C029 책 먹는 여우** (프란치스카 비어만)
- **C030 점** (피터 H. 레이놀즈)
- 각 책 +21 토론 +20 퀴즈 +6 심화 = **235 항목 추가**
- 톤 가이드: 짧은 호흡 / 자기 경험 연결형 60%+ / 어려운 한자어 회피
- 자동 검수: 부적합 어휘(C029 "절망"→"슬퍼하기") 자동 교정

### 2. React error #310 잠재 버그 근본 수정
"단원별 추천보기" 진입 시 빈 화면 + Hooks count mismatch.
- **원인**: `CurriculumScreen()`을 conditional 렌더 안에서 함수 호출. 함수 안 `useState("1")`이 부모 BookQuest의 hook 슬롯에 잡혀서 화면 진입 시 hook count가 +1 → React error #310 throw.
- **해결**: `ProfileSetupScreen`이 이미 가지고 있던 우회 패턴(사전 호출 + 변수 보관) 그대로 `CurriculumScreen`에도 적용.
  ```js
  const profileSetupContent = ProfileSetupScreen();
  const curriculumContent = CurriculumScreen();   // ← 사전 호출 추가
  // ...
  {profile && screen === "curriculum" && curriculumContent}  // ← 변수 참조
  ```
- **교훈**: `<XScreen />` JSX vs `XScreen()` 함수호출 구분. 함수호출 + 내부 hooks 조합은 항상 conditional 렌더에서 #310 위험. **새 Screen 추가 시 반드시 같은 사전 호출 패턴 적용 필요**.

### 3. CurriculumScreen 데이터 모델 전환 — 단원 → 책 (책 → 단원 태그)
빈 단원·중복 책 노출 문제 근본 해결.
- **기존**: 학기 토글 → 단원 리스트 → 단원별 추천 책 (단원이 주, 책이 종)
- **신규**: 학년별 책 6권 카드 → 카드마다 학기·단원 태그 (책이 주, 단원이 메타)
- **데이터 소스**: `CURRICULUM_BOOKS[].curriculumLinks` 직접 활용 (CURRICULUM_MAP은 단원 제목 lookup용으로만 보조)
- **부수 효과**: 빈 단원 자동 안 보임, 같은 책 여러 단원 매핑이 자연스럽게 표시됨, 책 활용도 한눈에 파악
- **UI**: 학기 토글 제거. 카드 안에 "#1학기 4단원 낱말과 만나요" 식 작은 태그 줄

### 4. 백로그 #002 등록 — 교과 연계 도서 학년별 12권 확장
`아이디어_백로그.md` 추가.
- 현재 학년별 6권 → **12권**으로 2배 확장 목표
- 단원 매핑 다양성 확보 + 학년 안에서 학생 선택지 풍부화
- Phase B 톤 가이드 그대로 적용 가능

### 5. Layer 1.5 Phase B Round 2 — 초2 6권 풀 25/25/8 확장
- **C031 만복이네 떡집** (김리리)
- **C032 나쁜 어린이표** (황선미)
- **C033 수박 수영장** (안녕달)
- **C034 잘못 뽑은 반장** (이은재)
- **C035 종이 봉지 공주** (로버트 문치)
- **C036 이상한 과자가게 전천당** (히로시마 레이코)
- 각 책 +21 토론 +20 퀴즈 +6 심화 = **282 항목 추가**
- 자동 검수: C035 "본질"→"안의 마음", "비극적"→"슬픈" 자동 교정
- "고정관념"은 원본 keyPoints/summary에도 있는 책 핵심 표현이라 보존 (검수 화이트리스트)

---

## 핵심 인프라 (이전 세션 + 이번 세션 누적)

### `app.html` 유틸 함수 (이전 세션 도입, 그대로 사용 중)
```js
const ALLOWED_LEVELS = { "1": ["easy"], ..., "중3": ["hard","expert"] };
const filterByLevel = (items, userGrade) => { ... };
const stableHash = (text) => { ... };
const prioritizeByUsedSet = (items, getKey, usedSetMap, seed) => { ... };
```

### state (Firestore 백업 포함, 이전 세션)
- `quizSeenMap`, `discussionSeenMap`, `deepSeenMap` — used-set
- `quizShuffleSeed`, `discussionShuffleSeed`, `deepShuffleSeed` — 셔플 안정화

### 이번 세션 신규 패턴
- **사전 호출 패턴 (React #310 회피)** — 새 화면 컴포넌트가 hook을 사용하면 반드시 `const xxxContent = XScreen();` 으로 사전 호출 후 conditional 렌더에서 변수 참조
- **CurriculumScreen 새 데이터 모델** — `CURRICULUM_BOOKS[].curriculumLinks`를 책 중심으로 역매핑

---

## 다음 세션 시작 시 이어서 할 일 (우선순위)

### 즉시 할 일
1. **Layer 1.5 Phase B Round 3 — 초3 6권 풀 25/25/8 확장**
   - C037~C042 추정 (학년 식별 먼저)
   - 같은 흐름: 메타 분석 → 282 항목 → splice → 검수 → push
   - 초2 톤 가이드 + 약간 더 풍부한 어휘
   - 작업 가이드: `outputs/phaseB_grade2_pools.py` 패턴 그대로 복제

2. **Layer 1.5 Phase B Round 4~7 — 초4 / 초5 / 초6 / 중1·중2·중3**
   - 학년별로 라운드 나눠 진행 (한 라운드 = 6권 = 한 세션 분량)
   - 시즌2 lower/upper/middle 16권씩은 라운드 8~10
   - 시즌2 도서는 `level` 태그 적용 필수 (단 이전 세션 grade_level_guide.md 분실 시 C001/C025/C049 패턴 참고)

3. **deprecated meta 태그 fix** (1분)
   - `<meta name="apple-mobile-web-app-capable">` 외에 `<meta name="mobile-web-app-capable">` 추가
   - 콘솔 경고 1개 정리

### [수동 — 사용자가 직접]
4. **표지 이미지 수집 — 78권** (`BookQuest_표지수집목록.docx` 활용)
5. **UI 아이콘 재크롭 + 배경 투명화**
6. **배틀 아바타 공격 컷신 이미지 생성** (나노바나나)

### 장기 과제
- **백로그 #002 — 교과 연계 도서 학년별 6권 → 12권 확장** (Phase B 끝난 뒤)
- Layer 2 — 응답시간 모니터링 + 챕터별 시퀀스 (진짜 독서 검증)
- Layer 3 — Spaced Repetition (망각곡선)
- 콘텐츠 풀이 50+로 커지면 → app.html에서 책 콘텐츠 별도 JSON 분리 (Babel 500KB 경고 대응)
- 시즌3 도서 큐레이션 (16주 신규 16권)
- 출판사 파트너십 / 교육청 연계

---

## 작업 가이드 문서 (outputs/)

- `phaseB_grade1_pools.py` — 초1 5권 풀 추가분 (235 항목)
- `phaseB_grade1_splice.py` — 풀 binary splice 표준 스크립트
- `phaseB_grade2_pools.py` — 초2 6권 풀 추가분 (282 항목)

→ 다음 라운드 시작 시 `phaseB_grade2_pools.py`를 학년만 바꿔 복제 + 학년별 책 ID 매핑 + 콘텐츠 작성. splice 스크립트 그대로 재사용.

→ 톤 표준은 이미 확장된 책(C001/C025/C049/C026~C030/C031~C036)의 토론·퀴즈·심화 패턴을 grep으로 추출해 모방.

---

## 데이터 현황

| 항목 | 권수 / 사이즈 |
|---|---|
| CURRICULUM_BOOKS | 54권 (C001~C054) |
| SEASON1_BOOKS | 13권 |
| SEASON2_BOOKS | 48권 |
| **C001 마당을 나온 암탉 풀** | **25/25/15 확장** (Phase A) |
| **C025 강아지똥 풀** | **25/25/8 확장** (Phase A) |
| **C026~C030 초1 5권 풀** | **25/25/8 확장** (Phase B Round 1) |
| **C031~C036 초2 6권 풀** | **25/25/8 확장** (Phase B Round 2) |
| **C049 데미안 풀** | **25/25/15 확장** (Phase A) |
| 나머지 책 (C037~C048, C050~C054, S1, S2) | 5/5/3 (Phase B 대기) |
| CURRICULUM_MAP 학년 | 9개 (1·2·3·4·5·6·중1·중2·중3) |
| FREE_BOOK_IDS | 동적 매핑 (CURRICULUM_BOOKS 모두 포함) |
| **app.html** | **~1.375 MB** (1,375,387 bytes) |
| **CurriculumScreen** | **책 중심 구조로 전환** |

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html                           # 메인 앱 (단일 파일 React PWA, ~1.375 MB)
├── index.html                         # 랜딩 페이지
├── sw.js                              # Service Worker
├── manifest.json                      # PWA 매니페스트
├── firestore.rules                    # Firestore 보안 규칙
├── firebase.json
├── .nojekyll                          # GitHub Pages Jekyll 비활성화
├── deploy.ps1                         # 배포 자동화 + sanity check
├── 아이디어_백로그.md                  # #001 유튜브 숏츠, #002 도서 12권 확장
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
| 책 상세 토론/퀴즈/심화 탭 | `bookTab === "discuss"/"quiz"/"deep"` IIFE |
| **CurriculumScreen (책 중심 구조)** | **~15083줄** |
| **사전 호출 패턴 (#310 회피)** | **~15599줄 메인 렌더링 직전** |

---

## 배포 명령어

```powershell
cd C:\dev\bookquest
.\deploy.ps1 "feat: 어떤 변경"
```

Sanity check 단계가 OK여야 push 진행. 빨간 XX는 push 중단.

---

## 주의사항 / 알려진 이슈

- **app.html이 ~1.375 MB로 커짐** — Edit tool로 수정 시 끝부분 잘림 / NULL 패딩 사례 자주 발생
  - 대량 변경은 Python splice로 binary mode 처리
  - deploy.ps1 sanity check가 1차 가드 (size + </html> + no NULL padding)
  - NULL 패딩 발견되면 Python으로 `.rstrip(b'\x00')` 후 다시 write
- **새 Screen 컴포넌트 추가 시** — hook 사용한다면 반드시 사전 호출 패턴. conditional 렌더는 변수만 참조. 직접 함수 호출하면 React error #310 위험.
- **한글 파일명 OK** (.nojekyll 덕분)
- **Cowork sandbox는 git 작업 권한 제한** — `.git\index.lock` 잔재 deploy.ps1이 자동 정리. .bak 백업은 마운트 권한 거부될 수 있음 (git이 대신함)
- **Babel script 500KB 초과 경고** — 동작 영향 없음, 장기적으로 콘텐츠 JSON 분리 필요
- **`apple-mobile-web-app-capable` deprecated 경고** — 동작 영향 없음, 1줄 fix 가능 (다음 세션 즉시 처리 권장)

---

## 풀 검수 체크리스트 (다음 라운드용)

splice 후 확인:
1. `</html>` 종료 + NULL 패딩 없음
2. 6권 객체 `{} []` 균형 OK
3. 6권 객체 단독 JS literal `node --check` 통과
4. 풀 카운트 (25/25/8) 6권 모두 ✓
5. choice 퀴즈 `answer` 인덱스가 `options` 범위 안
6. 학년별 부적합 어휘 grep:
   - **초저학년 (1·2·3)**: 본질, 정체성, 비극적, 절망, 우울, 윤리적, 천착, 대두, 보편적
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
| ca35073 | feat: Phase B Round 2 초2 6권 풀 25/25/8 |

---

## 이전 세션에서 누적된 핵심 (보존)

### Layer 1 — 출제 풀 셔플 + used-set
- 부분 표시: 토론 5→3, 퀴즈 5→4, 심화 3→2
- 셔플 우선순위: 안 본 항목 → 오래 본 항목 → 최근 본 항목
- "🔄 다른 주제 보기" 버튼
- used-set Firestore 백업

### 학년별 난이도 필터
- `ALLOWED_LEVELS` / `filterByLevel`
- `level` 없는 항목은 모든 학년 노출 (교과 연계 호환)

### 프로필 학년 9개 통일 + 빠른 학년 변경 위젯 (관리자 전용)

### 배포 자동화 — `deploy.ps1`
- 잔재 정리 / SW 캐시 bump / sanity check / git push
- UTF-8 BOM (한글 메시지 안전)

### 버그 수정 (이전)
- SW 외부 origin 통과
- Firestore 보안 규칙
- app.html truncation 가드
