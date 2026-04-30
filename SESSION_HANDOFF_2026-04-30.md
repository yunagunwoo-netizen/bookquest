# SESSION HANDOFF — 2026-04-30

> AI 환각 도서 정리 + 경기도교육청 추천도서 큐레이션

## ⭐ 핵심 변경 요약

오늘은 BookQuest의 도서 데이터를 **AI 환각 위험에서 분리**하는 대규모 정리 작업이 있었음. 사용자(김아빠)가 「200권 모두 AI 생성」이라는 사실을 인지하고 신뢰성 회복을 위한 의사결정을 내림.

**최종 방향**:
- 시즌1 BOOKS pool 13권 (= 사용자가 PDF로 보유한 진짜 책) **유지**
- CURRICULUM_BOOKS 108권 + SEASON2_BOOKS 48권 (AI 생성 환각 위험) → **ARCHIVE로 보존, 앱 비노출**
- 경기도교육청 7년치 추천도서 캡처 21장 → 사용자가 직접 텍스트로 정리한 578권 → **96권으로 큐레이션** (학년 16권, 학기 8권)
- 중학생 콘텐츠 picker UI 제거 (대상 = 초1~초6)

## 📂 오늘 생성·수정된 파일

### 신규
- `ocr_results/user_provided_books.txt` — 사용자가 정리한 578권 원본
- `ocr_results/parsed_books.json` — 파싱·dedup된 578권
- `ocr_results/classified_books.json` — 8 도메인 분류
- `ocr_results/curated_96_books.json` — 최종 큐레이션 96권
- **`ocr_results/curated_96_books.xlsx`** ⭐ — 사용자가 검토할 엑셀 (8 시트)
- `recommended_lists/` — 사용자 업로드 21장 캡처 (PNG)
- `recommended_lists_enlarged/` — 확대본 (vision 가독성↑)
- `scripts/ocr_recommended_books.js` — Anthropic vision OCR 스크립트 (현재 키 401 미작동)
- `backup/pre_purge_20260430_074824/` — 작업 전 백업 (app.html, app-data.js, covers/)

### 수정
- `app.html`
  - `findBookById`: ARCHIVE에서도 검색 (배지·전적 historical 호환)
  - `CURRENT_SEASON`: 2 → 1 (시즌2 비노출 처리, BOOKS 13권 사용)
  - `_safeSeasonBooks`: seasonBooks 빈 배열 시 BOOKS 폴백 (크래시 방지)
  - ScheduleScreen 교과 연계 섹션: `findBookById` → `ALL_BOOKS.find` (archive 노출 차단)
  - 중학생 picker UI 3곳 제거 (회원가입·프로필 수정·시그업)
  - 프로필 아바타 선택: `!storeHidden` 필터 추가 (브롤스타즈 숨김), `portrait={true}` 추가
  - closing tags 복구
- `app-data.js`
  - `CURRICULUM_BOOKS` → `_CURRICULUM_BOOKS_ARCHIVE` 이름 변경
  - `SEASON2_BOOKS` → `_SEASON2_BOOKS_ARCHIVE` 이름 변경
  - 파일 끝에 `const CURRICULUM_BOOKS = []` / `const SEASON2_BOOKS = []` 추가 (display용 빈 배열)

## 🔧 알아야 할 기술적 이슈

### 1. Edit 도구 트렁케이션 버그
- 큰 파일 (app.html 11K+ 줄)에서 Edit 도구가 끝부분을 잘라먹는 현상 반복
- 해결: **반드시 Python으로 안전 편집 + Sanity check** (`tail -3` 으로 `</html>` 확인)
- backup/ 디렉토리에 작업 전 스냅샷 보관

### 2. Anthropic API 키 401 Unauthorized
- console.anthropic.com에 잔액 $4.82 정상, 키 정상 발급
- 그러나 모든 키 (bookquest_3, bookquest_4) 401 거절
- 응답이 정상 JSON이 아닌 평문 「Unauthorized」 → **sandbox 환경 프록시 가로채기 의심**
- 해결: **사용자 PC에서 직접 Node.js 스크립트 실행** 필요
- `scripts/ocr_recommended_books.js` 준비됨

### 3. 환경 차단 (sandbox)
- Anthropic API: 도달은 하지만 401 (프록시 가로채기?)
- Google Gemini API: 403 Tunnel Forbidden (완전 차단)
- 알라딘 API: 같은 사용자 PC에서만 작동 (이전 fetch_aladin_covers.js와 동일)

### 4. AnySign4PC 파일 연결
- `.env` 파일이 Windows에서 「AnySign4PC 암호화」 프로그램과 연결됨 (시각적 이슈, 실제 파일은 plain text)
- 사용자가 .env 더블클릭하면 암호 창 뜸 → 우클릭 → 「프로그램에서 열기」 → 「메모장」 권장

### 5. functions/.env 위치
- API 키들이 root `.env`(빈 파일)가 아닌 `functions/.env`에 저장됨 (Firebase Functions용)
- `CLAUDE_KEY`, `GEMINI_KEY`, `OPENAI_KEY`, `ELEVENLABS_KEY` 다 있음
- TTS_ENGINE 줄 뒤에 NULL 바이트 68개 있는데 무시해도 됨

## 📊 현재 데이터 상태

### 시즌1 BOOKS pool (앱 노출, 13권)
| id | title | author |
|---|---|---|
| 1 | 청소년을 위한 외교광장 | 남기정 외 |
| 2 | 씨앗을 부탁해 | (저자) |
| 3 | 생각이 크는 인문학: 우주 | (저자) |
| 4 | 선생님, 노동이 뭐에요? | 하종강 |
| 5 | 법의학이야기 | 유성호 |
| 6 | 좋은 돈 나쁜 돈 이상한 돈 | 권재원 |
| 7 | 좋아요가 왜 안 좋아? | (저자) |
| 8 | 지구에서 가장 큰 발자국 | (저자) |
| 9 | 미래를 살리는 착한 소비 이야기 | 한화주 |
| 10 | 뇌과학과 인공지능 | 이대열 |
| 11 | 우리가 꼭 알아야 할 판결 | (저자) |
| 12 | 동방견문록 | (저자) |
| 13 | 궁금해요 세금과 나라살림 | (저자) |

### PDF는 있는데 BOOKS에 미등록 4권 (id 14~17 신규 추가 예정)
- 공정무역 세계여행
- 빅데이터
- 세상에서 가장 슬픈 여행자 난민
- 어린이를 위한 동물복지 이야기

### Archive (앱 비노출, 데이터 보존)
- `_CURRICULUM_BOOKS_ARCHIVE`: 108권 (C001~C108)
- `_SEASON2_BOOKS_ARCHIVE`: 48권 (id 2101~2316)

### 큐레이션 96권 (추가 예정, 메타데이터만)
- `ocr_results/curated_96_books.xlsx` 사용자 검토 대기 중
- 학년 16권 × 6학년 = 96권
- 학기 8권 × 2학기
- 옵션 1 차등 배분 (어린 학년은 문학·환경·과학 비중↑)

## 🚀 다음 세션 시작 시 해야 할 일

### Step 1 — 사용자 엑셀 검토 결과 확인
- `ocr_results/curated_96_books.xlsx` 사용자가 수정한 버전 받기
- 도메인 잘못 분류된 책, 부적절한 책 교체 등

### Step 2 — 96권 메타데이터를 app-data.js에 통합 (옵션 A)
- 새 const `RECOMMENDED_BOOKS` 또는 기존 풀에 추가
- ID 부여 (예: R001~R096)
- BookQuest 책 객체 형식으로 변환 (title, author, grade, semester, domain, ...)
- 콘텐츠 (chapters/summary/quizzes/discussionTopics/deepQuestions)는 일단 placeholder 또는 「준비중」 안내

### Step 3 — UI 통합
- HomeScreen 또는 새 「교과연계 추천」 화면에서 96권 노출
- 무료 액세스 (기획대로)
- 책 클릭 시 「콘텐츠 준비중」 또는 책 소개만

### Step 4 — 알라딘 표지 자동 수집 (옵션 B, 선택)
- `scripts/fetch_aladin_covers.js` 응용
- 96권 ISBN 검색 → 표지 다운로드
- `covers/R001.jpg ~ R096.jpg`로 저장

### Step 5 — 17권 PDF 콘텐츠 검증 (별개 작업)
- `책데이터/` 17권 PDF → pdfplumber 텍스트 추출
- BOOKS pool 13권 + 신규 4권 (id 14~17) 콘텐츠 검증·재생성
- Anthropic API 필요 → 키 401 문제 해결 후 진행

### Step 6 — 알라딘·Anthropic API 키 문제 해결
- console.anthropic.com에서 새 키 발급 후 functions/.env 업데이트
- 사용자 PC에서 OCR/검증 스크립트 실행 (sandbox 우회)

## 🎯 사용자 결정사항 (꼭 따를 것)

1. **교과연계 도서는 무료** — 수익은 시즌별 도서에서
2. **96권이 적당** (학년 16권 = 학기 8권 × 2)
3. **검증 작업을 사용자가 하지 않음** — 출시 전 자동으로 다 정리하고 가야 함
4. **사용자 = 검증 인력 X** — 신고 버튼 같은 거 절대 X
5. **17권 PDF만이 진짜 보유 책** — 그 외엔 콘텐츠 환각 위험
6. **대상 = 초1~초6 한정** (중학생은 향후 확장 여지만)

## 📝 운영 정보

- 베타 사용자: 김건우 (yunagunwoo@gmail.com 자식, 초2)
- 김건우 진행률 데이터는 작업 중 깨져도 OK (사용자 명시)
- Firebase Hosting: bookquest.co.kr
- GitHub: yunagunwoo-netizen/bookquest
- API 키 다 functions/.env에 저장 (CLAUDE_KEY, GEMINI_KEY, OPENAI_KEY, ALADIN_KEY, ELEVENLABS_KEY)

## 🔥 알려진 위험·주의사항

- ⚠️ Edit 도구로 큰 파일 편집 시 트렁케이션 — Python 사용 권장
- ⚠️ deploy.ps1은 sanity check 통과해야 push (size > 500KB, ends with `</html>`, no NULL padding)
- ⚠️ Anthropic 401 — 새 키 발급해도 sandbox에서 작동 안 할 수 있음, 사용자 PC 필요
- ⚠️ findBookById가 ARCHIVE도 검색하므로 historical 데이터 (배지·전적) 호환됨, 그러나 표시 코드에서 ARCHIVE 책 노출 안 되도록 `ALL_BOOKS`만 사용

---

# 2026-04-30 (PM 추가 작업) — RECOMMENDED 96권 통합 + EXTRA 4권 등록

> 오늘 후속 세션에서 진행. 96권 풀 통합 + UI 화면 + PDF 보유 4권 메타 등록 + 알라딘 스크립트 준비

## ⭐ 핵심 변경

1. **RECOMMENDED_BOOKS 96권 통합** — 사용자 검토 없이 그대로 진행 결정
2. **「교과연계 추천도서」 UI 화면 신설** — HomeScreen 진입 카드 + RecommendedBooksScreen
3. **EXTRA_BOOKS 4권 신규 등록** — id 14~17, 사용자 PDF 보유, 시즌 외 별도 풀
4. **알라딘 표지 자동 수집 스크립트** 준비 — 사용자 PC에서 실행 필요
5. **Edit 도구 트렁케이션 2회 발생** — git 백업으로 복구, 이후 Python으로만 편집

## 📂 추가/수정된 파일 (오늘 PM)

### 신규
- `scripts/fetch_aladin_covers_recommended.js` — 96권 표지 자동 수집 스크립트

### 수정
- `app-data.js`
  - 끝에 `const RECOMMENDED_BOOKS = [ ... 96권 ... ]` 추가 (R001~R096)
  - 끝에 `const EXTRA_BOOKS = [ ... 4권 ... ]` 추가 (id 14~17, PDF 보유 보너스)
  - 사이즈: 2,336,374 → 2,367,746 bytes
- `app.html`
  - line 1005~1007: `_SAFE_RECOMMENDED`, `_SAFE_EXTRA` 헬퍼 + `ALL_BOOKS`에 통합
  - line 2582: `BOOK_COVERS`에 14~17 + R001~R096 매핑 100개 추가
  - line 3175: `isRecommendedBook` 헬퍼 + `FREE_BOOK_IDS`에 RECOMMENDED·EXTRA 96+4=100권 무료
  - HomeScreen 끝부분에 「교과연계 추천도서 96권」 진입 카드
  - `RecommendedBooksScreen` 컴포넌트 신설 (학년/학기/도메인 필터 + 책 그리드 + 모달)
  - 라우팅: `screen === "recommended"` 추가
  - 하단 네비: recommended는 home의 자식으로 표시
  - 사이즈: 724,808 → 741,671 bytes

## 📊 현재 데이터 상태 (2026-04-30 PM)

| 풀 | 수량 | 상태 | id 형식 |
|---|---|---|---|
| BOOKS (시즌1) | 13 | 노출, 콘텐츠 풍부 | 1~13 (정수) |
| EXTRA_BOOKS (보너스) | 4 | 노출, 콘텐츠 placeholder | 14~17 (정수) |
| RECOMMENDED_BOOKS | 96 | 노출, 메타만 (무료) | R001~R096 (문자열) |
| CURRICULUM_BOOKS (display) | 0 | 비노출 | — |
| SEASON2_BOOKS (display) | 0 | 비노출 | — |
| _CURRICULUM_BOOKS_ARCHIVE | 108 | 비노출 (배지·전적용) | C001~C108 |
| _SEASON2_BOOKS_ARCHIVE | 48 | 비노출 (배지·전적용) | 2101~2316 |

ALL_BOOKS 합산 = 13 + 4 + 0 + 96 = **113권** (unique IDs 모두 검증됨)

## 🔧 RecommendedBooksScreen UI 동작

- 진입: HomeScreen 노란 그라데이션 카드 클릭 → `setScreen("recommended")`
- 필터: 학년 6탭 (1~6) → 학기 3탭 (전체/1학기/2학기) → 도메인 9버튼 (전체+8영역)
- 표시: 책 카드 그리드 2열, 표지 placeholder (도메인 컬러 + 이모지) — covers/Rxxx.jpg가 있으면 자동 덮어씀
- 책 클릭 → 상세 모달 (메타정보 + 「줄거리·퀴즈·토론은 점차 추가됩니다」 안내)
- 무료 라벨 명시 (수익 모델은 시즌별 도서)

## 🔥 EXTRA_BOOKS (보너스 4권) 메타

| id | 제목 | 페이지 | 도메인 | 비고 |
|---|---|---|---|---|
| 14 | 공정무역 세계여행 | 152 | economy+history | mlkit 스캔 PDF, 텍스트 레이어 X |
| 15 | 빅데이터 | 136 | science+media | mlkit 스캔 PDF |
| 16 | 세상에서 가장 슬픈 여행자 난민 | 107 | philosophy+history | mlkit 스캔 PDF |
| 17 | 어린이를 위한 동물복지 이야기 | 164 | environment+philosophy | mlkit 스캔 PDF |

- 저자·출판사는 빈 문자열 (알라딘 스크립트로 자동 채울 예정)
- 콘텐츠(chapters/summary/quizzes)는 빈 배열 + `contentReady: false`
- `bonus: true` 플래그로 시즌 진행도와 분리

## 🚀 다음 세션 시작 시 해야 할 일

### Step 1 — 사용자 PC에서 알라딘 표지 + 메타 수집
```powershell
cd C:\dev\bookquest
$env:ALADIN_KEY = "ttb_xxx"   # https://www.aladin.co.kr/ttb/wblog_manage.aspx 에서 발급
node scripts/fetch_aladin_covers_recommended.js
```
- 96권 (R001~R096) 표지 자동 다운로드 → `covers/Rxxx.jpg`
- `covers_missing_R.json` 누락분 직접 처리
- 기존 `scripts/fetch_aladin_covers.js`로 EXTRA 4권 (id 14~17)도 수집 가능 (BOOKS 추출 시 자동 포함)

### Step 2 — EXTRA 4권의 저자·출판사 채우기
- 알라딘 검색 결과에서 자동 매칭 또는 사용자가 직접 입력
- `app-data.js`의 EXTRA_BOOKS 객체 author/publisher 필드 업데이트

### Step 3 — 17권 PDF 콘텐츠 검증·재생성 (별개)
- `책데이터/` 폴더의 17개 PDF는 모두 mlkit 스캔본 (텍스트 레이어 없음)
- OCR 필요 → Anthropic Vision API 또는 Google Vision API
- Anthropic 키 401 문제 해결 후 사용자 PC에서 실행
- 재생성된 콘텐츠는 BOOKS·EXTRA의 빈 chapters/summary/quizzes 채움

### Step 4 — 96권 콘텐츠 단계적 추가 (장기)
- 무료 노출 유지하되 「콘텐츠 준비중」 → 점차 책 줄거리·핵심 질문·퀴즈 추가
- 자동 생성은 환각 위험 0%여야 함 (PDF 본문 OCR 후 그것 기반만)

### Step 5 — deploy 후 실기 확인
```powershell
.\deploy.ps1
```
- bookquest.co.kr에서 HomeScreen → 노란 카드 → 96권 화면 동작 확인
- 학년·학기·도메인 필터 + 책 모달 정상 작동 확인
- 베타 사용자(김건우 초2)는 1학년 16권 또는 2학년 16권 보임

## ⚠️ 알려진 함정 (재확인)

- ⚠️ **Edit 도구 트렁케이션 두 번 발생** — 큰 파일에서 끝부분 잘라먹음. 반드시 Python (`with open ... 'wb'`) 사용
- ⚠️ **Write 도구 한글 손상** — 가끔 UTF-8 깨뜨림. 한글 많은 파일은 Python으로 작성
- ⚠️ functions/.env에 ALADIN_KEY 없음 — 사용자가 알라딘 OpenAPI에서 직접 발급 후 추가 필요
- ⚠️ PDF 17권 모두 mlkit 스캔본 — 텍스트 레이어 X, OCR 필수

## 📋 sanity check 결과 (오늘 PM 끝 시점)

```
app.html: 741,671 bytes / </html> ✓ / NULL 0 / >500KB ✓
BOOKS: 13 / EXTRA: 4 / RECOMMENDED: 96 / ARCHIVE: 108+48
ALL_BOOKS 합산 = 113권 (unique IDs 100% 검증)
BOOK_COVERS 매핑: 13(시즌1) + 4(EXTRA) + 96(RECOMMENDED) + 기타
모든 변경사항 정상 적용
```


## 🔄 2026-04-30 (PM 후속) — 알라딘 표지 수집 + R020·R071 교체

사용자가 PC에서 `node scripts/fetch_aladin_covers_recommended.js` 실행 → 96권 중 2권(R020, R071)이 알라딘 검색 실패. 같은 학년·도메인 내에서 다른 책으로 교체.

### 교체 내역

| id | 학년/학기/도메인 | Before | After |
|---|---|---|---|
| R020 | 2학년 / law | 소중한 나 (제시카 산더스, 북멘토, 2019) | **우주에서 찾아온 특별한 나** (류미정, 뭉치, 2023, borrowed_from_grade=1) |
| R071 | 5학년 / philosophy | 키라의 감정학교 시리즈 (최형미, 을파소, 2018) | **나를 표현하는 열두 가지 감정** (임성관, 책속물고기, 2018) |

교체 후 다시 알라딘 스크립트 실행 → 96권 모두 표지 수집 완료.

### 동기화된 파일
- `app-data.js` (RECOMMENDED_BOOKS R020, R071 객체 갱신)
- `ocr_results/curated_96_books.json` (books[19], books[70] 갱신, R020에 borrowed_from_grade=1 추가)
- `covers/R020.jpg`, `covers/R071.jpg` (새 책 표지로 갱신됨)

### 교훈
- 알라딘 OpenAPI는 잘 알려진 베스트셀러·메이저 출판사 책에 강함, 마이너 출판사·신간이 아닌 책에 약함
- 큐레이션 시점에 알라딘 검색 가능성도 일부 고려하면 좋을 듯 (다음 큐레이션 시 참고)
