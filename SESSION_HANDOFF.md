# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29

---

## 이번 세션에서 완료한 작업

### 1. 교과 연계 도서 초1~중3 전학년 확장 (#49)
- **CURRICULUM_BOOKS**: 24권 → **54권** (C001~C054)
  - 신규 추가 30권: 초1, 초2, 초3, 중2, 중3 (각 학년 1·2학기 3권씩)
- **CURRICULUM_MAP**: 4·5·6·중1 → **1·2·3·4·5·6·중1·중2·중3 (9개 학년)**
- **FREE_BOOK_IDS**: 동적 매핑(`...CURRICULUM_BOOKS.map(b => b.id)`) — 자동 포함
- **2022 개정 교육과정** 기준 단원·주제 매핑

### 2. 시즌2 도서 48권 책별 맞춤 콘텐츠 생성 (#50)
- 기존: 모든 시즌2 도서가 템플릿화된 더미 콘텐츠
- 변경: 48권 모두 책별 실제 내용 기반 풀세트 콘텐츠 (chapters / summary / keyPoints / discussionTopics / quizzes)
- 티어 구성 그대로: lower 16권 / upper 16권 / middle 16권

#### 중복 도서 정리 (3건)
| 시즌2 ID | 기존 책 | 교체 후 | 이유 |
|---|---|---|---|
| 2107 | 강아지똥 | 100만 번 산 고양이 (사노 요코) | C025와 중복 |
| 2108 | 구름빵 | 엄마 자판기 (조경규) | C027과 중복 |
| 2316 | 데미안 | 갈매기의 꿈 (리처드 바크) | C049와 중복 |

### 3. 표지 이미지 수집용 워드 파일 생성
- `BookQuest_표지수집목록.docx` (74KB)
- 신규 교과 연계 30권 + 시즌2 48권 = 78권 정리
- 학년/티어별 그룹, 검색 키워드, 체크박스 포함

### 4. GitHub Pages 빌드 실패 해결
- `.nojekyll` 파일 생성 → Jekyll 빌드를 건너뛰고 정적 파일 그대로 서빙
- 한글 파일명에 의한 인코딩 오류로 빌드 실패하던 문제 해결
- 사용자가 PowerShell에서 push 필요

### 5. Service Worker 캐시 버전 업데이트
- 새 버전: `bookquest-v20260429014413`

---

## 미해결 / 사용자 처리 필요

### 배포 (사용자가 PowerShell에서 직접 실행 필요)

코워크 sandbox는 git 권한 제한으로 push를 못 합니다. **PowerShell에서 직접 실행:**

```powershell
cd C:\dev\bookquest
Remove-Item -ErrorAction SilentlyContinue sw.js.bak
Remove-Item -ErrorAction SilentlyContinue .git\index.lock
git add -A
git commit -m "feat: 시즌2 48권 책별 맞춤 콘텐츠 생성, 중복 도서 3건 정리, .nojekyll 추가"
git push origin main
```

### 배포 후 확인사항
- 브라우저 하드 리프레시(Ctrl+Shift+R)로 최신 SW 적용
- GitHub Pages 빌드가 ✓ green으로 끝나는지 확인 ([Actions 페이지](https://github.com/yunagunwoo-netizen/bookquest/actions))
- 시즌2 도서 상세 화면에서 책별 콘텐츠가 정상 출력되는지 확인 (이전엔 모두 같은 템플릿이었음)
- 신규 교과 연계 도서 30권 (C025~C054) 학년별 정상 표시 확인

---

## 다음 세션 할 일 (우선순위 순)

### 즉시 할 일
1. **[수동] 교과 연계 도서 + 시즌2 도서 표지 이미지 수집** (#47, 신규)
   - `BookQuest_표지수집목록.docx` 활용 — 78권 목록 정리됨
   - 알라딘·교보문고에서 검색 → `book_<ID>.jpg` 형식으로 저장

2. **[수동] UI 아이콘 재크롭 + 배경 투명화 처리** (#48)
   - 아이콘 다시 자르고 배경 투명화 작업

3. **[수동] 배틀 아바타 공격 컷신 이미지 생성** (#52)
   - 나노바나나로 캐릭터별 공격 컷신 이미지 생성

### 장기 과제
- [1000명 달성 후] 출판사 파트너십 제안 (#17)
- [장기] 교육청/교과서 출판사 공식 연계 (#18)
- [장기] 시즌3 도서 큐레이션 (16주 신규 16권)

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html              # 메인 앱 (단일 파일 React PWA, ~935KB)
├── index.html            # 랜딩 페이지
├── sw.js                 # Service Worker
├── manifest.json         # PWA 매니페스트
├── .nojekyll             # GitHub Pages Jekyll 빌드 비활성화 (신규)
├── BookQuest_표지수집목록.docx  # 78권 표지 수집 가이드 (신규)
├── icons/
│   ├── ui/               # UI 아이콘 PNG
│   └── v1/               # 버전1 에셋
├── skills/
│   └── bookquest-season-builder/
│       └── SKILL.md      # 시즌 도서 자동화 스킬
└── 앱스크린샷_*.jpg       # 랜딩페이지 스크린샷
```

## 주요 코드 위치 (app.html)

| 구조 | 위치 (대략) |
|------|------|
| SEASONS / CURRENT_SEASON | ~661줄 |
| GRADE_TO_TIER / getTier | ~665줄 |
| CURRICULUM_MAP (9개 학년) | ~682줄 |
| CURRICULUM_BOOKS C001~C054 | ~830줄~ |
| SEASON2_BOOKS (48권 맞춤 콘텐츠) | ~4250줄~ |
| getSeasonBooks / getAllBooksForGrade | SEASON2_BOOKS 직후 |
| FREE_BOOK_IDS (동적 매핑) | CURRICULUM_BOOKS 이후 |

## 데이터 현황

| 항목 | 권수 |
|---|---|
| CURRICULUM_BOOKS (교과 연계) | 54권 (C001~C054) |
| SEASON2_BOOKS (시즌2) | 48권 (lower 16 / upper 16 / middle 16) |
| CURRICULUM_MAP 학년 | 9개 (1·2·3·4·5·6·중1·중2·중3) |
| FREE_BOOK_IDS | 자동 매핑 (CURRICULUM_BOOKS 모두 포함) |
| 중복 도서 | 0건 (CURRICULUM ↔ SEASON2 교차 검증 완료) |

## 배포 명령어 (PowerShell)

```powershell
cd C:\dev\bookquest; $ts=(Get-Date -Format 'yyyyMMddHHmmss'); (Get-Content sw.js -Raw) -replace "bookquest-v\d{14}","bookquest-v$ts" | Set-Content sw.js; git add -A; git commit -m "커밋 메시지"; git push origin main
```

## 주의사항

- **app.html 편집 시 truncation 위험**: 파일이 ~935KB로 크므로, 대량 삽입은 Python splice 스크립트 사용 권장
- **한글 파일명 OK**: `.nojekyll` 추가로 한글 파일명도 자유롭게 사용 가능
- **SW 캐시**: 배포 후 반영이 안 되면 하드 리프레시(Ctrl+Shift+R) 또는 SW Unregister
- **Cowork sandbox는 git 작업 권한 제한**: app.html / sw.js 수정은 가능하지만 git commit/push는 PowerShell에서 실행
- **sw.js 파일 인코딩 주의**: UTF-8이 아닌 인코딩으로 저장되어 있으니 직접 편집 시 주의 (스크립트로 수정 시 binary 모드 권장)
