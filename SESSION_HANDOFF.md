# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-30 (라운드 3 완료) — CURRICULUM 신규 5·6학년 12권 + 교체 2권 풀 25/25/8 확장

---

## 이번 세션에서 완료한 작업 (오늘 한 줄 요약)

**작업 8 commits**: SEASON2 upper 풀 → SEASON2 middle 풀 → 시즌2 라이브 오픈(hotfix 후) → CURRICULUM 54→108권 큐레이션 → CURRICULUM 신규 1·2학년 풀. 현재 풀 25/25/8 도달 책: **127권 / 169권** (BOOKS 13 + CURRICULUM 66 + SEASON2 48). 시즌2 라이브 노출 시작.

### 1. SEASON2 upper 16권 풀 25/25/8 (+800 항목)
- 2201~2216 (초3-6 학년군)
- 풀 5/3/0 → 25/25/8 (deepTopics 키 신규 추가)
- 6건 quiz q 충돌(보편 q "이 책의 작가는?" 등) → dedupe 후 통과
- commit `7b5ee13`

### 2. 백업 파일 cleanup + .gitignore 패턴 추가
- `app-data.js.bak.before_upper`가 같이 커밋된 이슈 → 제거
- `.gitignore`에 `*.bak.*` 추가 — 이후 모든 라운드의 백업 자동 제외
- commit `ddbb9b3`

### 3. SEASON2 middle 16권 풀 25/25/8 (+800 항목)
- 2301~2316 (중1-3 학년군)
- 사전 회피 패턴 도입 — overview 단계에서 기존 quiz q 추출 → 풀 작성 시 회피
- **충돌 0건으로 한 번에 통과** (사전 회피 패턴 효과 입증)
- commit `944fcfa`

### 4. ⭐ 시즌2 라이브 오픈 (CURRENT_SEASON 1→2)
- 첫 시도: PowerShell `(Get-Content -Raw) -replace ... | Set-Content -NoNewline` 사용 → app.html이 17 KB 손상되어 화면 빈 백색 (commit `2409072`)
- revert (commit `246ca76`)
- 재시도: **Python binary write** (`raw.replace(b'CURRENT_SEASON = 1;', b'CURRENT_SEASON = 2;')`)로 정확히 1바이트만 변경 → 시즌2 정상 오픈 (commit `77ba000`)

### 5. ⭐ CURRICULUM 54 → 108권 확장 (+54 신규 + 2 교체)
- 학년별 6권 → **12권** (1~6학년·중1~중3 모두 12권 균등)
- C018(5학년 "우리들의 일그러진 영웅" 중복) → **어린이를 위한 한국 미술사** (art, history)
- C022(중1 "소나기" 중복) → **청소년을 위한 한국 음악사** (art, history)
- C055~C108: 신규 54권 (메타 + 풀 5/3/0)
- 8대 지식 영역 균형: economy/environment/law/media/sociology가 0권 → 7~11권
- splice 시 trailing comma 처리 버그 1회 발생(109권 sparse array) → last char 검증 분기 추가
- commit `ee75ea8`

### 6. 백로그 #002 후속 — 라운드 1 (1·2학년 12권 풀 25/25/8 +600 항목)
- C055~C066 (12권) 풀 5/3/0 → 25/25/8
- 사전 회피 dedupe 9건 (보편 q "이 책의 형식/메시지/분야는?" 등) → 처리 후 0건
- commit `8a0d79a`

### 7. 백로그 #002 후속 — 라운드 2 (3·4학년 12권 풀 25/25/8 +600 항목)
- C067~C078 (12권) 풀 5/3/0 → 25/25/8
- 사전 회피 dedupe 12건 (라운드 1 9건과 비슷한 양) → 처리 후 0건
  - 11건은 기존 q 충돌, 1건은 INTRA-NEW-DUP (C078 disc·deep 동일 q)
- 8대 지식 영역 균형: history×3, economy×2, environment×2, media×2, law×2, sociology×2, science×3, art×1
- 톤: 3·4학년 — 일상 비유, 과학·역사·환경 풍부, 약간의 추상 OK
- `.gitignore`에 누락된 `*.bak.*` 패턴 재추가 (이전 핸드오프에 반영했지만 실제 파일에서 누락 발견)
- 검증 통과: BOOKS=13, CURRICULUM=108, SEASON2=48, 12권 25/25/8, answer/dup/regression/NULL=0
- app-data.js: 1,906,461 → 2,028,909 bytes (+121,448)
- commit `a7401da`

### 8. 백로그 #002 후속 — 라운드 3 (5·6학년 12권 + 교체 2권 풀 25/25/8 +700 항목)
- C079~C090 (12권) + C018·C022 (교체 2권) 풀 5/3/0 → 25/25/8
- 14권 × 50항목 = 700 신규
- 사전 회피 dedupe 31건 (1차 27건 + 2차 4건 — 보편 q + 두 책 사이 동일 q "이 책은 인권이 처음부터..." 분기 처리 + INTRA-NEW-DUP 1건) → 처리 후 0건
- 톤: 5·6학년 — 추상 어휘 OK (권력·공정함·보편적 권리·시민 자질), 사례 + 깊은 사고, 시민 자질 자극
- 8대 지식 영역 + 정체성: history×4, economy×2, environment×2, media×2, law×2, sociology×3, society×2, science×2, art×2 (음악사·미술사 포함)
- 검증 통과: BOOKS=13, CURRICULUM=108, SEASON2=48, 14권 25/25/8, answer/dup/regression/NULL=0
- app-data.js: 2,028,909 → 2,169,102 bytes (+140,193)

---

## 핵심 인프라

### 데이터 파일 구조
```
C:\dev\bookquest\
├── app.html        # React PWA 코드 (~708KB, Babel 변환)
├── app-data.js     # 책 데이터 (~1.91MB, 일반 script, 글로벌 const)
├── sw.js           # Service Worker (cache list에 app-data.js 포함)
└── ...
```

`app-data.js`는 다음 세 글로벌 const를 선언:
```js
const CURRICULUM_BOOKS = [...];  // 108권 (라운드1 후)
const BOOKS = [...];             // 시즌1 13권
const SEASON2_BOOKS = [...];     // 48권
```
Babel script(`<script type="text/babel">`) 안에서 직접 참조함 (재선언 없음).

### 시즌 전환 (현재 상태)
```js
const CURRENT_SEASON = 2;  // 시즌2 라이브 오픈됨
```
- 라이브에서 학년군별로 SEASON2 책이 노출됨
- SEASON2 lower/upper/middle 16권씩 모두 25/25/8 ✓

### 풀 splice 패턴 (라운드 1에서 확립)
- 대상: `app-data.js`의 `BOOKS` / `CURRICULUM_BOOKS` / `SEASON2_BOOKS` 배열
- 책 식별: 
  - SEASON2: `id: NNN` (numeric)
  - CURRICULUM: `id: "CNNN"` (string)
- 각 책 객체의 `quizzes` / `discussionTopics` / `deepTopics` 배열 닫는 `]` 직전에 새 항목 삽입
- deepTopics 키 부재 시 객체 닫는 `}` 직전에 신규 키+배열 추가
- splice 후 Node 단독 평가 → 풀 카운트·중복·answer 인덱스·regression·NULL 검증 → deploy
- **신규 항목 hint 어미는 "떠올려 봐"로 일관**

---

## 다음 세션 시작 시 이어서 할 일 (우선순위)

### 즉시 할 일 — 백로그 #002 후속 라운드 4 (마지막)
**라운드 4: CURRICULUM 신규 중1·중2·중3 18권 풀 25/25/8** (C091~C108)
- 책당 +22 disc + +20 quiz + +8 deep = 50 항목
- 18권 × 50 = **+900 항목**
- 톤: 중학생 — 학술 어휘 일부 OK, 진지함과 보편성, C049 데미안 패턴, 청소년 시민 톤
- 한 세션에 끝내기 부담 시 6 batches 3권씩 (C091~C093 / C094~C096 / ... / C106~C108)
- 라운드 4 완료 시 CURRICULUM 108권 모두 25/25/8 → **풀 25/25/8 합계 169권 / 169권 (100%)** 도달!

### 남은 작업
| 라운드 | 대상 | 항목 |
|---|---|---|
| 4 | C091~C108 (중1·중2·중3 18권) | +900 |
| **남음** | **18권** | **+900 항목** |

### 그 다음 (라운드 4 이후)
- **Layer 2**: 응답시간 모니터링 + 챕터별 시퀀스 (진짜 독서 검증)
- **Layer 3**: Spaced Repetition (망각곡선)

### [수동 — 사용자가 직접]
- 표지 이미지 수집 (SEASON1 13 + SEASON2 48 + CURRICULUM 신규 56권)
- UI 아이콘 재크롭 + 배경 투명화
- 배틀 아바타 공격 컷신 이미지 생성

---

## 작업 가이드 패턴 (다음 라운드용)

### 라운드 1에서 확립된 4 스크립트 (그대로 복제)
- `outputs/curriculum_round1_overview.py` — id 범위 + 컨텍스트 + 기존 q 추출
- `outputs/curriculum_round1_pools.py` — POOLS dict 형식 (책 id → discussions/deeps/quizzes)
- `outputs/curriculum_round1_splice.py` — CURRICULUM 패턴 binary splice
- `outputs/curriculum_round1_verify.js` — Node 검증 (카운트·중복·regression·NULL)

라운드 2~4는 id 범위만 바꿔서 복제하면 됨.

### 라운드 작업 흐름 (한 세션 안에 끝나는 페이스)
1. **컨텍스트 추출** — 12~18권 chapters/keyPoints/summary + 기존 5 quiz q + 3 disc q
2. **pools.py 4 batches로 작성** — 3~5권씩 batch (책당 50항목)
3. **사전 회피 dedupe** — 기존 q와 충돌하는 신규 q 다른 표현으로 변경
4. **splice 실행** — Python binary write, 백업 자동 (`.bak.before_round{N}`)
5. **Node 검증** — 모두 통과 확인
6. **Deploy** — `.\deploy.ps1 "feat: ..."`

### 풀 작성 톤 가이드 (학년군별)
| 학년 | 추상명사 정책 | 어조 |
|---|---|---|
| 1·2학년 (CURRICULUM lower) | 매우 보수적 — 본질·정체성·우울·비극 회피 | 일상 비유, 짧은 문장, 청유형 |
| 3·4학년 (라운드 2) | 일부 추상 OK — 과학·역사·환경 친근하게 | 사례 중심, 약간의 비유 |
| 5·6학년 (라운드 3) | 추상 어휘 OK — 사회·경제·법·미디어 개념 | 더 깊은 사고, 시민 자질 자극 |
| 중1~중3 (라운드 4) | 학술 어휘 일부 OK — 진지함과 보편성 | C049 데미안 패턴, 청소년 시민 톤 |

### 사전 회피 보편 q 패턴 (처음부터 변형 사용)
라운드 1에서 9건 충돌. 다음 라운드는 처음부터 다음 표현으로 작성:

| ❌ 충돌 자주 발생 | ✅ 회피 표현 (라운드 1 적용) |
|---|---|
| "이 책의 형식에 가장 가까운 것은?" | "이 책의 책 종류에 가장 가까운 것은?" |
| "이 책의 메시지에 가장 가까운 것은?" | "이 책이 보내는 핵심 메시지에 가장 가까운 것은?" |
| "이 책의 분야에 가장 가까운 것은?" | "이 책의 책 종류에 가장 가까운 것은?" |
| "이 책의 작가는?" | "이 책의 글쓴이는?" / "이 책을 쓴 사람은?" |
| "이 책의 작가는 한국인이다." | "이 책의 글쓴이는 한국에서 태어난 작가다." |
| "이 책이 강조하는 X에 가장 가까운 것은?" | "이 책이 그리는 X에 가장 가까운 것은?" |

### 검증 워크플로 (필수 체크리스트)
1. Node 단독 평가 통과
2. 책 수 보존 (BOOKS=13, CURRICULUM_BOOKS=108, SEASON2_BOOKS=48)
3. 변경 책의 풀 카운트 ≥ 25/25/8
4. choice answer 인덱스 0 ≤ ans < options.length
5. ox answer 타입 boolean
6. 책 내 q 중복 0건 (quiz/disc/deep 합쳐서)
7. 변경하지 않은 책 regression 0건
8. NULL byte 0개

---

## 데이터 현황 (라운드 3 완료 시점)

| 항목 | 풀 상태 |
|---|---|
| **CURRICULUM_BOOKS** | **108권** (학년별 12권 균등) |
| ↳ 25/25/8 도달 | 92권 (52 + C055~C078 라운드1·2 + C079~C090 + C018·C022 라운드3) |
| ↳ 5/3/0 대기 | 16권 (C091~C108) |
| **BOOKS (시즌1)** | 13권 모두 25/25/8 |
| **SEASON2 lower** | 16권 모두 25/25/8 |
| **SEASON2 upper** | 16권 모두 25/25/8 |
| **SEASON2 middle** | 16권 모두 25/25/8 |
| **CURRENT_SEASON** | **2** (시즌2 라이브 오픈) |
| **app.html** | 708,788 bytes |
| **app-data.js** | 2,169,102 bytes (라운드3 후) |
| **풀 25/25/8 합계** | **153권 / 169권 (90.5%)** |

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html                           # 메인 React 앱 (~708KB)
├── app-data.js                        # 책 데이터 글로벌 const (~1.91MB)
├── index.html                         # 랜딩 페이지
├── sw.js                              # Service Worker
├── manifest.json                      # PWA 매니페스트
├── firestore.rules                    # Firestore 보안 규칙
├── firebase.json
├── .nojekyll                          # GitHub Pages Jekyll 비활성화
├── .gitignore                         # *.bak.* 패턴으로 백업 자동 제외
├── deploy.ps1                         # 배포 자동화
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
| **CURRENT_SEASON 상수 (시즌 스위치)** | app.html ~685줄 (현재 2) |
| **CURRICULUM_BOOKS / BOOKS / SEASON2_BOOKS** | **app-data.js** (분리됨) |
| getSeasonBooks / findBookById | app.html ~ 이전 BOOKS 정의 자리 근처 |
| 책 상세 토론/퀴즈/심화 탭 | bookTab === "discuss"/"quiz"/"deep" IIFE |
| CurriculumScreen (책 중심) | app.html ~14000줄대 |
| 사전 호출 패턴 (#310 회피) | 메인 렌더링 직전 |
| 홈 교과 연계 grid 3분할 | 홈 카드 영역 |
| PWA 설치 배너 (한글 직접) | app.html `showInstallBanner && (() => ...` 부근 |

---

## 배포 명령어

```powershell
cd C:\dev\bookquest
.\deploy.ps1 "feat: 어떤 변경"
```

Sanity check 단계가 OK여야 push 진행. deploy.ps1은 app.html만 sanity 검증 — app-data.js는 Node 단독 평가로 사전 검증 필요.

---

## 주의사항 / 알려진 이슈 (lesson learned 누적)

- **PowerShell `Get-Content -Raw | Set-Content`는 한글 UTF-8 파일 파괴 위험** — 1줄 수정도 반드시 **Python binary write**로
  ```python
  raw = open('app.html','rb').read()
  raw = raw.replace(b'OLD_BYTES', b'NEW_BYTES')
  open('app.html','wb').write(raw)
  ```
- **`.gitignore`의 `*.bak.*` 패턴** = 모든 백업 파일 자동 제외 (deploy 깔끔)
- **사전 회피 dedupe** = overview에서 기존 quiz/disc q 추출 → pools 작성 시 회피하면 사후 dedupe 작업 최소화 (라운드 1 9건 → 다음 라운드 0~3건 예상)
- **CURRICULUM splice의 trailing comma 주의** — 마지막 객체 뒤 `,` 있는지 last char 검증 후 분기 처리
- **`git revert <hash> --no-edit && git push`** = hotfix 깔끔 패턴 (시즌2 오픈 깨짐 사례에서 검증)
- **app-data.js가 ~1.91MB로 큼** — Edit tool truncation 위험. 모든 변경 Python binary write 우선
- **deepTopics 키 부재 책** — splice 스크립트가 "키 추가" 분기 가져야 함 (라운드 1에서 검증된 패턴)
- **신규 풀 항목 hint 어미는 "떠올려 봐"로 통일** — dedupe 시 신규 byte 매칭에 도움
- **새 Screen 컴포넌트 추가 시** — hook 사용하면 반드시 사전 호출 패턴
- **Babel script 500KB 경고는 여전히 존재** (687KB) — 동작 영향 없음
- **Cowork sandbox는 git index.lock 권한 제한** — `git show HEAD:<path>` + Python binary write로 우회 가능
- **한글 파일명 OK** (.nojekyll 덕분)

---

## Git 커밋 히스토리 (이번 세션, 8 commits)

| commit | 메시지 |
|---|---|
| 7b5ee13 | feat: SEASON2 upper 16권(2201~2216) 풀 25/25/8 확장 (+~800) |
| ddbb9b3 | chore: 백업 파일 제거 + .gitignore에 *.bak.* 추가 |
| 944fcfa | feat: SEASON2 middle 16권(2301~2316) 풀 25/25/8 확장 (+~800) |
| 2409072 | feat: 시즌2 오픈 (CURRENT_SEASON 1→2) — PowerShell 인코딩 손상 발생 |
| 246ca76 | revert: 깨진 시즌2 오픈 되돌림 |
| **77ba000** | **feat: 시즌2 오픈 재시도 (Python binary write로 정확히 1바이트 변경)** |
| **ee75ea8** | **feat: CURRICULUM 54→108권 확장 — 학년별 12권, 8대 지식 영역 모두 채움 (+54 신규, C018·C022 중복 정리)** |
| 8a0d79a | feat: CURRICULUM 신규 1·2학년 12권(C055~C066) 풀 25/25/8 확장 (+600 항목) |
| a7401da | feat: CURRICULUM 신규 3·4학년 12권(C067~C078) 풀 25/25/8 확장 (+600 항목) |
| (다음) | feat: CURRICULUM 5·6학년 12권 + 교체 2권(C079~C090, C018, C022) 풀 25/25/8 확장 (+700 항목) |

---

## 이전 세션 누적 핵심 (보존)

### 이전 세션 — D2 데이터 분리 + SEASON2 lower 풀 (2026-04-29 저녁)
- 6 commits: deprecated meta fix → SEASON1 13권 풀 25/25/8 → PWA 배너 한글 수정 → app-data.js 데이터 분리 → SEASON2 lower 16권 풀
- BOOKS·CURRICULUM_BOOKS·SEASON2_BOOKS 정의를 app-data.js로 분리 (app.html -62%, Babel deopt 페널티 감소)
- SEASON2 lower 16권(2101~2116) 풀 25/25/8 (+~801)
- 21건 중복 dedupe로 처리

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
- UTF-8 BOM (한글 메시지 안전)

### 버그 수정 (이전)
- SW 외부 origin 통과
- Firestore 보안 규칙
- app.html truncation 가드
