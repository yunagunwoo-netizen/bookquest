# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29 (저녁) — D2 데이터 분리 + SEASON2 lower 풀 확장

---

## 이번 세션에서 완료한 작업 (오늘 한 줄 요약)

**작업 6 commits**: deprecated meta fix → SEASON1 13권 풀 25/25/8 → PWA 배너 한글 깨짐 수정 → **app-data.js 데이터 분리(인프라 큰 변경)** → SEASON2 lower 16권 풀 25/25/8. 현재 풀 25/25/8 도달 책: **83권** (SEASON1 13 + CURRICULUM 54 + SEASON2 lower 16).

### 1. deprecated meta 태그 fix
- `apple-mobile-web-app-capable` 그대로 + `mobile-web-app-capable` 추가 (1줄)
- 콘솔 경고 1개 정리

### 2. SEASON1 13권 풀 25/25/8 확장 (~585 항목)
- BOOKS 13권 모두 quizzes 25 / discussionTopics 25 / deepTopics 8 도달
- C012 동방견문록 quiz 1건 중복(쿠빌라이 칸) 자동 발견 → 다른 질문(원나라에서 머문 기간)으로 교체

### 3. PWA 설치 배너 한글 깨짐 수정
- JSX 텍스트 노드에 한글이 `\uXXXX` escape sequence로 적혀 있어 그대로 출력되던 버그
- 7곳(iOS·Chrome 배너 제목/부제/안내문/버튼 라벨) Python binary 치환으로 한글 직접 입력
- "BookQuest 설치하기 / 홈 화면에 추가하면 더 빠르게! / 닫기 / 설치" 정상 표시

### 4. ⭐ D2 — 책 데이터 app-data.js 분리 (큰 인프라 변경)
- `BOOKS` (시즌1 13) + `CURRICULUM_BOOKS` (54) + `SEASON2_BOOKS` (48) 정의를 `app-data.js`로 추출
- `app.html`에 `<script src="app-data.js"></script>`를 Babel script 직전에 삽입
- 일반 script로 로드되어 Babel 변환 대상에서 제외 — Babel script 1.84MB → 687KB (-62.5%)
- `app.html` 자체는 1.87MB → 708KB (-62%)
- `sw.js` ASSETS_TO_CACHE에 `./app-data.js` 추가
- Babel 500KB 경고는 여전히 표시(687KB도 한도 초과)되지만 deopt 페널티 자체는 큰 폭 감소
- **이후 모든 풀 작업 대상이 app.html → app-data.js로 변경됨**

### 5. SEASON2 lower 16권 풀 25/25/8 확장 (~801 항목)
- 2101~2116 (초1-2 그림책·동화·입문서)
- 기존 5/3/0 → 25/25/8 (deepTopics 키 자체가 없어 16권 모두 새로 추가)
- 21건 중복 자동 발견 → dedupe 스크립트로 모두 다른 질문으로 교체
- 신규 항목 hint 어미가 "떠올려 봐"로 일관 → 기존 "생각해 봐"와 구분되어 매칭 가능

### 6. 손상 working copy 복구 (세션 시작 직후 발견)
- 이전 세션 잔재로 app.html(40줄 truncation), sw.js(5줄 truncation), 아이디어_백로그.md(36줄 사라짐), NEXT_RELEASE.md(NULL 패딩)이 working copy에 남아 있던 상태
- `git show HEAD:<path>` + Python binary write로 4파일 모두 HEAD 복구 (lock 파일 권한 문제 우회)
- HEAD(d097937, v1.9.0)의 정상 상태에서 작업 재개

---

## 핵심 인프라

### 데이터 파일 구조 (D2 이후)
```
C:\dev\bookquest\
├── app.html        # React PWA 코드 (~708KB, Babel 변환)
├── app-data.js     # 책 데이터 (~1.32MB, 일반 script, 글로벌 const)
├── sw.js           # Service Worker (cache list에 app-data.js 포함)
└── ...
```

`app-data.js`는 다음 세 글로벌 const를 선언:
```js
const CURRICULUM_BOOKS = [...];  // 54권
const BOOKS = [...];             // 시즌1 13권
const SEASON2_BOOKS = [...];     // 48권
```
Babel script(`<script type="text/babel">`) 안에서 직접 참조함 (재선언 없음).

### `app.html` 유틸 함수 (이전부터 사용 중)
```js
const ALLOWED_LEVELS = { "1": ["easy"], ..., "중3": ["hard","expert"] };
const filterByLevel = (items, userGrade) => { ... };
const stableHash = (text) => { ... };
const prioritizeByUsedSet = (items, getKey, usedSetMap, seed) => { ... };
```

### 시즌 전환 (중요)
```js
const CURRENT_SEASON = 1;  // 운영 중인 시즌 (2로 바꾸면 시즌2 오픈)
```
- SEASON2_BOOKS 풀이 모두 채워진 후 이 값을 2로 변경하면 시즌2가 메뉴에 노출됨
- 현재는 **CURRENT_SEASON=1** 상태이므로 SEASON2 풀 추가는 사용자 화면에 즉시 보이지 않음 (백업 데이터로 GitHub에 안전하게 적재됨)

### 사전 호출 패턴 (React #310 회피)
- 새 Screen 컴포넌트가 hook 사용하면 메인 렌더링 직전 `const xxxContent = XScreen();` 사전 호출 후 변수 참조

### 풀 splice 패턴 (D2 이후)
- 대상: `app-data.js`의 `BOOKS` / `CURRICULUM_BOOKS` / `SEASON2_BOOKS` 배열
- 각 책 객체의 `quizzes` / `discussionTopics` / `deepTopics` 배열 닫는 `]` 직전에 새 항목 삽입
- 책 식별: `id: NNN` 매칭 (numeric)
- splice 후 Node로 단독 평가 → 풀 카운트·중복·answer 인덱스 검증 → deploy
- **신규 항목 hint 어미는 "떠올려 봐"로 일관** — 기존 "생각해 봐"와 구분되어 dedupe 시 신규 byte 매칭 쉬움

---

## 다음 세션 시작 시 이어서 할 일 (우선순위)

### 즉시 할 일 (모멘텀 유지)
1. **A-2 — SEASON2 upper 16권 풀 확장** (초3-6 톤)
   - 2117~2132? (실제 ID는 분석 시 확인) — 16권 × 50 항목 ≈ 800 항목
   - lower 패턴 그대로 복제: `season2_upper_overview.py` → `season2_upper_pools.py` → `season2_upper_splice.py` → dedupe → deploy
   - 톤: 초고학년 — 일부 추상명사 허용 (CURRICULUM 4·5·6 학년 패턴)

2. **A-3 — SEASON2 middle 16권 풀 확장** (중1-3 톤)
   - 16권 × 50 항목 ≈ 800 항목
   - 톤: 중학생 — 추상 어휘 허용 (SEASON1·CURRICULUM 중학교 패턴, C049 데미안 패턴)

3. **시즌2 오픈** (A-2, A-3 완료 후)
   - `app.html`에서 `CURRENT_SEASON = 1` → `CURRENT_SEASON = 2` 변경
   - 라이브에서 학년군별로 SEASON2 책이 노출됨

### 그 다음 (A-1~A-3 완료 후)
- **백로그 #002**: CURRICULUM 학년별 6권 → 12권 확장 (54권 → 108권 큐레이션 필요)
- **Layer 2**: 응답시간 모니터링 + 챕터별 시퀀스 (진짜 독서 검증)
- **Layer 3**: Spaced Repetition (망각곡선)

### [수동 — 사용자가 직접]
- 표지 이미지 수집 (기존 78권 + SEASON1 추가 13권 + SEASON2 48권)
- UI 아이콘 재크롭 + 배경 투명화
- 배틀 아바타 공격 컷신 이미지 생성

---

## 작업 가이드 패턴 (다음 라운드용)

### SEASON2 upper / middle 라운드 시작 시 복제할 스크립트
- `outputs/season2_lower_overview.py` — tier 필터해서 책 리스트 + 컨텍스트 JSON 추출
- `outputs/season2_lower_pools.py` — POOLS dict 형식 (책 id → discussions/deeps/quizzes)
- `outputs/season2_lower_splice.py` — app-data.js 대상 binary splice (deepTopics 신규 추가 처리 포함)
- `outputs/season2_lower_dedupe2.py` — 중복 탐지 후 신규 항목 byte 매칭으로 치환

### 풀 작성 톤 가이드 (학년군별)
| Tier | 추상명사 정책 | 어조 |
|---|---|---|
| lower (초1-2) | 매우 보수적 — 본질·정체성·우울·비극 회피 | 일상 비유, 짧은 문장, 청유형 |
| upper (초3-6) | 일부 추상명사 허용 — 사회·경제·과학 개념 OK | CURRICULUM 초고 패턴 참고 |
| middle (중1-3) | 추상 어휘 허용 — 학술용어는 제외 | C049 데미안 패턴, SEASON1 중학생 톤 |

### 검증 워크플로 (필수 체크리스트)
1. Node 단독 평가: `(function(){ ... ; return {...};})()`로 wrap 후 eval
2. 책 수 확인 (BOOKS=13, CURRICULUM_BOOKS=54, SEASON2_BOOKS=48)
3. 변경 대상 책의 quizzes/discussionTopics/deepTopics 길이 ≥ 25/25/8
4. choice answer 인덱스 0 ≤ ans < options.length
5. ox answer 타입 boolean
6. 책별 질문 중복 0건 (Map으로 q 텍스트 비교)
7. SEASON1·CURRICULUM regression 0건 (변경하지 않은 책의 풀 카운트 보존)
8. app-data.js NULL 0 / 합법 JS literal

### 중복 발생 패턴 (lower에서 학습)
- 풀 작성 시 기존 책 컨텍스트의 discussions/quizzes를 참고하다 같은 질문을 다시 적게 되는 경우 발생
- 신규 작성 hint 어미를 "떠올려 봐"로 일관하면 기존 "생각해 봐"와 byte 차이가 나서 신규만 매칭 가능
- dedupe 스크립트는 각 중복마다 신규 항목의 정확한 byte sequence를 만들어 1번 치환

---

## 데이터 현황

| 항목 | 풀 상태 |
|---|---|
| **CURRICULUM_BOOKS** | 54권 모두 25/25/8 (Phase B 전체) |
| **BOOKS (시즌1)** | 13권 모두 25/25/8 (오늘 SEASON1 라운드) |
| **SEASON2 lower** | 16권 모두 25/25/8 (오늘 A-1, deepTopics 신규) |
| **SEASON2 upper** | 16권 5/3/0 (A-2 대기) |
| **SEASON2 middle** | 16권 5/3/0 (A-3 대기) |
| **app.html** | 708,788 bytes (D2 이후) |
| **app-data.js** | 1,321,454 bytes (D2 + SEASON1 + SEASON2 lower) |

---

## 핵심 파일 구조 (갱신)

```
C:\dev\bookquest\
├── app.html                           # 메인 React 앱 (~708KB)
├── app-data.js                        # 책 데이터 글로벌 const (~1.32MB) [D2 신규]
├── index.html                         # 랜딩 페이지
├── sw.js                              # Service Worker (app-data.js 포함)
├── manifest.json                      # PWA 매니페스트
├── firestore.rules                    # Firestore 보안 규칙
├── firebase.json
├── .nojekyll                          # GitHub Pages Jekyll 비활성화
├── deploy.ps1                         # 배포 자동화 + sanity check
├── 아이디어_백로그.md
├── BookQuest_표지수집목록.docx
├── icons/
└── skills/
    └── bookquest-season-builder/SKILL.md
```

---

## 주요 코드 위치

| 구조 | 위치 |
|---|---|
| ALLOWED_LEVELS / filterByLevel | computeAvatarStats 직전 |
| stableHash / prioritizeByUsedSet | 같은 영역 |
| **CURRENT_SEASON 상수 (시즌 스위치)** | app.html ~685줄 |
| **CURRICULUM_BOOKS / BOOKS / SEASON2_BOOKS** | **app-data.js** (분리됨) |
| getSeasonBooks / findBookById | app.html ~ 이전 BOOKS 정의 자리 근처 |
| 책 상세 토론/퀴즈/심화 탭 | bookTab === "discuss"/"quiz"/"deep" IIFE |
| CurriculumScreen (책 중심) | app.html ~14000줄대 |
| 사전 호출 패턴 (#310 회피) | 메인 렌더링 직전 |
| 홈 교과 연계 grid 3분할 | 홈 카드 영역 |
| **PWA 설치 배너 (한글 직접)** | app.html `showInstallBanner && (() => ...` 부근 |

---

## 배포 명령어

```powershell
cd C:\dev\bookquest
.\deploy.ps1 "feat: 어떤 변경"
```

Sanity check 단계가 OK여야 push 진행. deploy.ps1은 app.html만 sanity 검증 — app-data.js는 Node 단독 평가로 사전 검증 필요.

---

## 주의사항 / 알려진 이슈

- **app-data.js가 ~1.32MB로 큼** — Edit tool truncation 위험은 app.html과 동일. 모든 변경 Python binary write 우선
- **SEASON2 풀 작업 시 deepTopics 키가 없는 책들 주의** — splice 스크립트가 "키 추가" 분기를 가져야 함 (lower 16권에서 검증된 패턴)
- **CURRENT_SEASON=2 전환은 SEASON2 모든 학년군(lower/upper/middle) 풀이 채워진 후에** — 부분 오픈 시 빈 학년군이 생겨 사용자 경험 저하
- **신규 풀 항목 hint 어미는 "떠올려 봐"로 통일** — dedupe 시 신규 byte 매칭에 도움
- **새 Screen 컴포넌트 추가 시** — hook 사용하면 반드시 사전 호출 패턴
- **Babel script 500KB 경고는 여전히 존재** (687KB) — 동작 영향 없음. 더 줄이려면 큰 React 컴포넌트의 별도 분리 또는 production build 도입 필요
- **Cowork sandbox는 git index.lock 권한 제한** — `git show HEAD:<path>` + Python binary write로 우회 가능
- **한글 파일명 OK** (.nojekyll 덕분)

---

## 풀 검수 체크리스트 (다음 라운드용)

splice + dedupe 후 확인:
1. Node 단독 평가 통과
2. 책 수 보존 (BOOKS=13, CURRICULUM_BOOKS=54, SEASON2_BOOKS=48)
3. 풀 카운트 (≥25/25/8) 모두 ✓
4. choice 퀴즈 answer 인덱스가 options 범위 안
5. 책별 풀 내 질문 중복 0건
6. SEASON1·CURRICULUM regression 0건
7. 학년별 부적합 어휘 grep:
   - **초저학년 (1·2·3, lower)**: 본질·정체성·비극적·절망·우울·윤리적·천착·대두·보편적
   - **초고학년 (4·5·6, upper)**: 좀 더 관대 — 추상명사 일부 허용
   - **중학생 (중1~3, middle)**: 추상 개념 허용 (C049 데미안 패턴 참고)
8. 원본 데이터(summary, keyPoints)에 이미 있는 단어는 화이트리스트로 보존

---

## Git 커밋 히스토리 (이번 세션, 6 commits)

| commit | 메시지 |
|---|---|
| 7d2c858 | fix: deprecated mobile-web-app-capable meta 태그 추가 |
| f1f1ca5 | feat: SEASON1 13권 풀 확장 — 모든 책 25/25/8 도달 (+585 항목) |
| 86e3994 | fix: PWA 설치 배너 한글 깨짐 수정 (JSX 텍스트 노드 \uXXXX → 한글) |
| **f1ada76** | **refactor: 책 데이터 app-data.js로 분리 (app.html -62%, Babel deopt 페널티 감소)** |
| ef5bd1e | feat: SEASON2 lower 16권(2101~2116) 풀 25/25/8 확장 (+~801, deepTopics 신규) |
| 00e4d02 | (sw cache bump only) |

---

## 이전 세션 누적 핵심 (보존)

### Phase B 전체 (2026-04-29 새벽~밤)
- CURRICULUM_BOOKS 54권 모두 25/25/8 풀 확장 (~2,400 항목)
- React #310 잠재 버그 근본 수정 (CurriculumScreen 사전 호출 패턴)
- CurriculumScreen 데이터 모델 전환 (단원→책 → 책→단원 태그)
- 홈 카드 grid 3분할
- v1.9.0 release

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
- UTF-8 BOOM (한글 메시지 안전)

### 버그 수정 (이전)
- SW 외부 origin 통과
- Firestore 보안 규칙
- app.html truncation 가드
