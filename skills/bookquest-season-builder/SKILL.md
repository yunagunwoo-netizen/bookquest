---
name: bookquest-season-builder
description: >
  BookQuest 시즌별 도서 큐레이션 및 콘텐츠 자동 생성 스킬.
  새 시즌 도서 리스트를 만들고, 각 책에 맞춤 콘텐츠(챕터/퀴즈/토론주제)를 생성하고,
  app.html에 통합하는 전체 워크플로우를 자동화합니다.
  "시즌 도서 추가", "새 시즌 만들기", "시즌3 도서 큐레이션", "책 콘텐츠 생성",
  "도서 리스트 업데이트" 등의 요청 시 이 스킬을 사용하세요.
  BookQuest 앱에 새 시즌 콘텐츠를 추가하는 모든 작업에 적극적으로 활용하세요.
---

# BookQuest 시즌 도서 빌더

BookQuest 앱의 시즌별 도서 큐레이션 + 콘텐츠 생성 + 코드 통합을 자동화하는 스킬입니다.

## 앱 구조 이해

BookQuest는 **단일 파일 React PWA** (`app.html`, ~13,500줄)입니다.

### 핵심 데이터 구조

```
SEASONS 객체: 시즌별 설정 (주수, 시작일, 티어 사용 여부)
CURRENT_SEASON: 현재 운영 중인 시즌 번호
BOOKS 배열: 시즌1 도서 13권 (티어 없음)
SEASON2_BOOKS 배열: 시즌2 도서 48권 (티어별 16권)
CURRICULUM_BOOKS 배열: 교과연계 도서 (무료, C001~C024)
```

### 티어 시스템

시즌2부터 학년군별 도서 분리:

| 티어 | 학년 | ID 범위 (시즌N) |
|------|------|-----------------|
| lower (초저) | 초1-2 | N101-N116 |
| upper (초고) | 초3-6 | N201-N216 |
| middle (중등) | 중1-3 | N301-N316 |

ID 규칙: `시즌번호` + `티어코드(1/2/3)` + `주차(01-16)`

### 8대 지식영역

economy, environment, science, law, history, media, philosophy, literature

시즌 도서는 이 8개 영역을 **골고루** 커버해야 합니다 (교과연계 도서는 literature/philosophy에 편중되어 있어서, 유료 시즌 도서가 나머지 영역을 채워주는 것이 프리미엄 모델의 핵심).

---

## Phase 1: 도서 리스트 큐레이션

### 입력 필요 정보

시작 전에 다음을 확인하세요:

- **시즌 번호** (예: 3)
- **주 수** (기본 16주)
- **시작 날짜** (예: "2027-03-01")
- **큐레이션 방식**: 웹 검색 기반 / 사용자 직접 제공 / 혼합

### 큐레이션 기준

각 티어(초저/초고/중등)에 대해 `주 수`만큼의 도서를 선정합니다.

**균형 원칙:**
- 8대 영역이 가능한 한 균등 분포 (16주 기준 영역당 2권)
- 각 티어의 난이도가 해당 학년군에 적합
- 한국에서 구할 수 있는 도서 우선
- 번역서와 국내 저자 도서 혼합

**도서 정보 수집 항목:**
- 제목, 부제, 저자, 페이지수
- 주요 영역 (domains: 최대 3개, 첫 번째가 메인)
- 테마 색상 (color: CSS gradient 문자열)
- 이모지 (emoji: 책 내용을 대표하는 이모지 1개)

### 출력 형식

Python 스크립트로 JavaScript 배열을 생성합니다. 직접 app.html을 편집하면 파일 크기 문제로 truncation이 발생할 수 있으므로, **반드시 Python 스크립트를 사용**하세요.

```python
books = []
for tier_code, tier_name, tier_books in [...]:
    for i, book in enumerate(tier_books):
        books.append(f"""  {{
    id: {season}{tier_code}{str(i+1).zfill(2)},
    week: {i+1},
    season: {season},
    tier: "{tier_name}",
    title: "{book['title']}",
    subtitle: "{book['subtitle']}",
    author: "{book['author']}",
    pages: {book['pages']},
    color: "{book['color']}",
    emoji: "{book['emoji']}",
    domains: {book['domains']},
    ...
  }}""")
```

---

## Phase 2: 책별 맞춤 콘텐츠 생성

각 도서에 대해 다음 콘텐츠를 생성합니다:

### 콘텐츠 구조

```javascript
{
  chapters: [
    { title: "1장 제목", summary: "1장 요약 (2-3문장)" },
    { title: "2장 제목", summary: "2장 요약 (2-3문장)" },
    { title: "3장 제목", summary: "3장 요약 (2-3문장)" }
  ],
  summary: "전체 줄거리 요약 (3-4문장)",
  keyPoints: ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
  discussionTopics: [
    "토론 주제 1 (열린 질문 형태)",
    "토론 주제 2",
    "토론 주제 3"
  ],
  quizzes: [
    {
      question: "퀴즈 질문",
      options: ["선택지1", "선택지2", "선택지3", "선택지4"],
      answer: 0  // 정답 인덱스
    },
    // ... 총 3개
  ]
}
```

### 콘텐츠 생성 가이드라인

- **챕터**: 실제 책의 구조를 반영하되, 3개로 압축. 각 장의 핵심 주제를 잘 드러내는 제목.
- **요약**: 스포일러 최소화, 책을 읽고 싶게 만드는 톤. 해당 학년군 수준의 어휘 사용.
- **핵심 포인트**: 책에서 배울 수 있는 가장 중요한 3가지. 8대 지식영역과 연결.
- **토론 주제**: 정답이 없는 열린 질문. 아이들이 자기 생각을 말할 수 있는 주제.
- **퀴즈**: 책 내용 이해도 확인. 너무 어렵지 않게, 핵심 내용 중심.

### 티어별 어조

| 티어 | 어휘 수준 | 문장 길이 |
|------|----------|----------|
| lower | 초1-2 수준, 쉬운 단어 | 짧고 간결 |
| upper | 초3-6 수준, 일부 전문용어 허용 | 보통 |
| middle | 중등 수준, 전문용어 활용 | 길고 복합적 허용 |

### 생성 방법

48권(16주 × 3티어)을 한꺼번에 생성하면 컨텍스트가 부족합니다. **티어별로 나누어** 생성하세요:

1. lower 티어 16권 콘텐츠 생성 → Python 스크립트로 JS 코드 출력
2. upper 티어 16권 → 같은 방식
3. middle 티어 16권 → 같은 방식

각 배치에서 Python 스크립트를 사용하여 JavaScript 코드를 파일로 출력하고, 마지막에 합칩니다.

---

## Phase 3: 앱 코드 통합

### 주의: 대형 파일 편집

app.html은 ~13,500줄, ~800KB입니다. 직접 Edit 도구로 대량 삽입하면 truncation 위험이 있습니다.

**권장 방법: Python splice 스크립트**

```python
import re

# 1. 현재 app.html 읽기
with open('app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 2. 새 시즌 도서 배열을 앵커 포인트 뒤에 삽입
anchor = "// === SEASON N BOOKS ==="  # 삽입 위치 마커
new_books_js = """
const SEASON{N}_BOOKS = [
  ... (생성된 도서 데이터)
];
"""

# 3. 삽입
content = content.replace(anchor, anchor + '\n' + new_books_js)

# 4. SEASONS 객체에 새 시즌 추가
# 5. findBookById에 새 배열 추가
# 6. getSeasonBooks에 새 시즌 분기 추가

# 7. 저장
with open('app.html', 'w', encoding='utf-8') as f:
    f.write(content)
```

### 코드 변경 체크리스트

새 시즌 추가 시 수정해야 할 곳:

1. **SEASONS 객체**: 새 시즌 설정 추가
2. **SEASON{N}_BOOKS 배열**: 도서 데이터 삽입
3. **findBookById**: 새 배열 검색 추가
4. **getSeasonBooks**: 새 시즌 분기 추가
5. **getAllBooksForGrade**: 필요 시 업데이트
6. **computeAvatarStats**: 새 배열 포함
7. **AskBookScreen**: 새 배열 검색 범위 추가

### 검증

통합 후 반드시 확인:

```python
# 파일 무결성 검증
with open('app.html', 'r', encoding='utf-8') as f:
    content = f.read()

assert '</html>' in content, "파일이 잘렸습니다!"
assert f'SEASON{N}_BOOKS' in content, "도서 배열이 없습니다!"
assert content.count(f'season: {N}') >= expected_count, "도서 수가 부족합니다!"
print(f"✅ 검증 통과: {len(content):,} bytes, {content.count(chr(10)):,} lines")
```

### sw.js 캐시 버전 업데이트

배포 전 `sw.js`의 `CACHE_NAME`을 새 타임스탬프로 변경:

```javascript
const CACHE_NAME = 'bookquest-v{YYYYMMDDHHMMSS}';
```

---

## 빠른 시작 예시

사용자: "시즌3 도서를 만들어줘"

1. 시즌3 설정 확인 (주수, 시작일)
2. 8대 영역 균형 맞춰 티어별 16권씩 큐레이션 (웹 검색 활용)
3. 사용자 검토 → 수정
4. 48권 콘텐츠 생성 (티어별 배치)
5. Python splice로 app.html에 통합
6. 무결성 검증
7. sw.js 캐시 버전 업데이트

---

## 참고: 색상 팔레트

도서별 color 필드에 사용할 수 있는 그라디언트 예시:

```
"linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
"linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
"linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
"linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
"linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
"linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)"
"linear-gradient(135deg, #fccb90 0%, #d57eeb 100%)"
"linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"
```

영역별로 일관된 색상 톤을 사용하면 시각적 구분에 도움됩니다:
- economy: 녹색/민트 계열
- environment: 초록/청록 계열  
- science: 파랑/보라 계열
- law: 네이비/인디고 계열
- history: 갈색/골드 계열
- media: 핑크/마젠타 계열
- philosophy: 보라/라벤더 계열
- literature: 코랄/살몬 계열
