# BookQuest 세션 핸드오프

> 최종 업데이트: 2026-04-29

---

## 이번 세션에서 완료한 작업

### 교과 연계 도서 초1~중3 전학년 확장 완료 (#49 / #36 일부)

- **CURRICULUM_BOOKS**: 24권 → **54권** (C001~C054)
  - 신규 추가 30권: 초1, 초2, 초3, 중2, 중3 (각 학년 1·2학기 3권씩)
- **CURRICULUM_MAP**: 4·5·6·중1 → **1·2·3·4·5·6·중1·중2·중3 (9개 학년)**
- **FREE_BOOK_IDS**: 동적 매핑(`...CURRICULUM_BOOKS.map(b => b.id)`)으로 자동 포함됨 (별도 수정 불필요)
- **2022 개정 교육과정** 기준 단원·주제 매핑

#### 추가된 도서 목록 (학년별)

| 학년 | ID | 도서 |
|---|---|---|
| 초1 1학기 | C025~C027 | 강아지똥 / 무지개 물고기 / 구름빵 |
| 초1 2학기 | C028~C030 | 알사탕 / 책 먹는 여우 / 점(The Dot) |
| 초2 1학기 | C031~C033 | 만복이네 떡집 / 나쁜 어린이표 / 수박 수영장 |
| 초2 2학기 | C034~C036 | 잘못 뽑은 반장 / 종이 봉지 공주 / 이상한 과자가게 전천당 |
| 초3 1학기 | C037~C039 | 아홉 살 마음 사전 / 칠판에 딱 붙은 아이들 / 푸른 사자 와니니 |
| 초3 2학기 | C040~C042 | 책과 노니는 집 / 마법의 설탕 두 조각 / 찰리와 초콜릿 공장 |
| 중2 1학기 | C043~C045 | 어린 왕자 / 페인트 / 동백꽃 |
| 중2 2학기 | C046~C048 | 모모 / 우아한 거짓말 / 우리들의 일그러진 영웅 |
| 중3 1학기 | C049~C051 | 데미안 / 아몬드 / 운수 좋은 날 |
| 중3 2학기 | C052~C054 | 동물농장 / 메밀꽃 필 무렵 / 나의 라임오렌지나무 |

각 도서마다 기존 C001~C024와 동일한 풀세트 콘텐츠(chapters / summary / keyPoints / characters / discussionTopics / deepTopics / quizzes)를 작성. 한국 작가 우선·해외 명작 보완 원칙으로 큐레이션.

### Service Worker 캐시 버전 업데이트
- 새 버전: `bookquest-v20260429004224`

---

## 미해결 / 사용자 처리 필요

### 배포 (사용자가 PowerShell에서 직접 실행 필요)

코워크 sandbox가 git 권한 문제로 자동 commit/push를 못 함. **PowerShell에서 직접 실행:**

```powershell
cd C:\dev\bookquest
# 잔여 백업 파일 정리 (있을 경우)
Remove-Item -ErrorAction SilentlyContinue sw.js.bak
Remove-Item -ErrorAction SilentlyContinue .git\index.lock
# git commit + push
git add -A
git commit -m "feat: 교과 연계 도서 초1~중3 전학년 확장 (24→54권), CURRICULUM_MAP 5개 학년 추가"
git push origin main
```

> SW 캐시 버전은 이미 `bookquest-v20260429004224`로 업데이트 되어 있으므로 추가 작업 없이 위 3줄만 실행하면 됩니다.

### 배포 후 확인사항
- 브라우저 하드 리프레시(Ctrl+Shift+R)로 최신 SW 적용
- 홈 화면에서 학년 1~중3 모든 학년이 도서 목록을 정상 표시하는지 확인
- 각 신규 도서 상세에서 chapters / quizzes 등 콘텐츠 정상 출력 확인
- CURRICULUM_MAP 단원별 추천도서가 정상 매칭되는지 한두 학년 샘플 확인

---

## 다음 세션 할 일 (우선순위 순)

### 즉시 할 일
1. **[수동] 시즌2 도서 48권 책 표지 이미지 수집 + 적용** (#47)
   - 실제 책 표지 이미지를 웹에서 다운받아 적용

2. **[수동] UI 아이콘 재크롭 + 배경 투명화 처리** (#48)
   - 아이콘 다시 자르고 배경 투명화 작업 (사용자 직접 수행)

3. **[수동] 교과 연계 도서 30권 책 표지 이미지 수집** (신규)
   - 신규 추가된 C025~C054의 실제 책 표지 이미지 수집·적용
   - 현재는 emoji + color로 처리되고 있음

4. **시즌2 도서 48권 책별 맞춤 콘텐츠 생성** (#50)
   - chapters, summary, keyPoints, discussionTopics, quizzes를 책 실제 내용 기반으로 생성
   - 실제 책 내용 없어도 공개 정보 기반으로 생성 가능

5. **[수동] 배틀 아바타 공격 컷신 이미지 생성** (#52)
   - 나노바나나로 캐릭터별 공격 컷신 이미지 생성

### 장기 과제
- [1000명 달성 후] 출판사 파트너십 제안 (#17)
- [장기] 교육청/교과서 출판사 공식 연계 (#18)

---

## 핵심 파일 구조

```
C:\dev\bookquest\
├── app.html              # 메인 앱 (단일 파일 React PWA, ~903KB / 약 14,500줄)
├── index.html            # 랜딩 페이지
├── sw.js                 # Service Worker (캐시 버전 관리)
├── manifest.json         # PWA 매니페스트
├── icons/
│   ├── ui/               # UI 아이콘 PNG
│   └── v1/               # 버전1 에셋 (shop_btn_bg.png 등)
├── skills/
│   └── bookquest-season-builder/
│       └── SKILL.md      # 시즌 도서 자동화 스킬
├── screenshot_battle1.jpg
├── screenshot_battle2.jpg
└── 앱스크린샷_*.jpg       # 랜딩페이지 스크린샷
```

## 주요 코드 위치 (app.html)

| 구조 | 위치 (대략) |
|------|------|
| SEASONS / CURRENT_SEASON | ~661줄 |
| GRADE_TO_TIER / getTier | ~665줄 |
| CURRICULUM_MAP (1·2·3·4·5·6·중1·중2·중3) | ~682줄 |
| CURRICULUM_BOOKS C001~C054 | ~830줄~ |
| SEASON2_BOOKS (48권) | ~2700줄 부근 (콘텐츠 추가로 줄 번호 이동) |
| getSeasonBooks / getAllBooksForGrade | SEASON2_BOOKS 직후 |
| FREE_BOOK_IDS (동적 매핑) | CURRICULUM_BOOKS 이후 |
| computeAvatarStats | ~3900줄 부근 |

## 배포 명령어 (PowerShell)

```powershell
cd C:\dev\bookquest; $ts=(Get-Date -Format 'yyyyMMddHHmmss'); (Get-Content sw.js -Raw) -replace "bookquest-v\d{14}","bookquest-v$ts" | Set-Content sw.js; git add -A; git commit -m "커밋 메시지"; git push origin main
```

## 주의사항

- **app.html 편집 시 truncation 위험**: 파일이 ~903KB로 크므로, 대량 삽입은 Python splice 스크립트 사용 권장
- **한글 파일명 주의**: 웹 서빙 시 인코딩 문제 발생 가능 → 영문 파일명 사용
- **SW 캐시**: 배포 후 반영이 안 되면 하드 리프레시(Ctrl+Shift+R) 또는 SW Unregister
- **Cowork sandbox는 git 작업 권한 제한**: app.html / sw.js 수정은 가능하지만 git commit/push는 PowerShell에서 실행
