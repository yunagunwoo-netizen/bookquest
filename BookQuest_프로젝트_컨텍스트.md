# BookQuest 프로젝트 컨텍스트

## 프로젝트 개요
- **이름**: BookQuest (북퀘스트) — 게이미피케이션 독서/토론 앱
- **대상**: 초6~중학생 (현재 사용자: 건우)
- **배포 URL**: https://yunagunwoo-netizen.github.io/bookquest/
- **호스팅**: GitHub Pages (프론트엔드) + Firebase Cloud Functions (백엔드)
- **기술 스택**: React 18 (CDN + Babel standalone), 단일 index.html 파일 (~3,737줄, ~4MB)

---

## 🚨 Claude 작업 규칙 (필독 — 세션마다 지킬 것)

### 규칙 1: git 명령은 **절대** bash에서 실행하지 않는다
- **이유**: Claude의 bash는 리눅스 샌드박스에서 도는데 `C:\dev\bookquest`는 윈도우 마운트. 리눅스 쪽 git이 만드는 `.git/index.lock` 등 임시 파일이 윈도우 ACL과 맞지 않아 리눅스 쪽에서 삭제 불가 → 락이 남으면 다음 git 작업이 전부 막힘.
- **허용**: bash에서는 Python/grep/ls/wc 등 **파일 내용 관련 작업만**.
- **금지**: `git status`, `git add`, `git commit`, `git push`, `git config`, `git diff` 등 **모든 git 명령**.
- **대신**: 커밋·푸시가 필요하면 **PowerShell 명령 블록**을 만들어 사용자에게 전달하고, 사용자가 PowerShell에서 직접 실행.

### 규칙 2: index.html (4.76MB)은 Edit 툴 사용 금지
- Edit 툴이 큰 파일에서 truncation 버그를 일으킴.
- **대신**: `cat > script.py << 'EOF' … EOF` 로 Python 패치 스크립트를 만들어 byte-level string replace 실행.

### 규칙 3: Write 툴은 8,692 바이트에서 잘림
- 그 이상은 bash heredoc (`cat > path << 'EOF'`) 사용.

### 규칙 4: 락 파일이 이미 남아있을 때 사용자에게 안내할 명령
```powershell
Remove-Item C:\dev\bookquest\.git\index.lock -Force
```
또는 `$PROFILE`에 `gitclean` 함수 등록해서 한 번에 정리.

---

## 핵심 파일 구조

### 메인 앱
| 파일 | 설명 |
|------|------|
| `index.html` | 메인 앱 (React SPA, 전체 코드 포함) |
| `manifest.json` | PWA 매니페스트 |
| `sw.js` | 서비스 워커 (캐시: bookquest-v2, network-first 전략) |
| `firebase.json` | Firebase 호스팅 설정 |
| `rollback.sh` | 브롤스타즈↔오리지널 캐릭터 전환 스크립트 |

### 백엔드 (Firebase Cloud Functions)
| 파일 | 설명 |
|------|------|
| `functions/index.js` | 373줄, Node.js 20 |
| `functions/.env` | API 키 (CLAUDE_KEY, ALADIN_KEY) |

**Cloud Functions 4개:**
1. `askBook` — 책 기반 Q&A (콜레트 선생님 페르소나, Claude API)
2. `discussionCoach` — 토론 코치 (칼 선생님 페르소나, Claude API)
3. `recommendBooks` — 책 추천 (바이런 선생님 + 알라딘 API)
4. `textToSpeech` — TTS (Google Cloud ko-KR-Neural2-C 남성/A 여성)

### 백업 파일
- `index_brawlstars_backup.html` — 브롤스타즈 버전 백업
- `index_original_backup.html` — 오리지널 캐릭터 버전 백업
- `functions/index_brawlstars_backup.js` — 백엔드 브롤스타즈 버전
- `functions/index_original_backup.js` — 백엔드 오리지널 버전

### 리소스 폴더
- `avatars/` — 아바타 이미지 (base64 임베딩됨, 원본도 보관)
- `covers/` — 책 표지 (book1~5.jpg)
- `icons/` — 앱 아이콘, 테마 아이콘, 미션 아이콘 등
- `오리지날 캐릭터/` — 나노바나나로 생성한 오리지널 캐릭터 원본 이미지
- `_원본이미지/` — 원본 이미지 백업

---

## 현재 상태: 브롤스타즈 캐릭터 버전 활성화

### 선생님 캐릭터 3명 (NPC)
| 상수명 | ID | 이름 | 역할 | 색상 |
|--------|------|------|------|------|
| `COACH` | carl | 칼 선생님 | 토론 코치 | #2196F3 |
| `RECOMMENDER` | byron | 바이런 선생님 | 책 추천가 | #764ba2 |
| `BOOK_HELPER` | colette | 콜레트 선생님 | 책 도우미 (Q&A) | #E040A0 |

각 캐릭터는 표정 시스템 보유 (default, speaking, thinking, happy, excited 등 — `COACH_IMGS`, `BOOK_HELPER_IMGS`, `RECOMMEND_IMGS` 상수에 base64 이미지 저장)

### 플레이어 아바타 5개 (`AVATAR_DATA`, 라인 822~)
shelly(쉘리), nita(니타), leon(레온), crow(크로우), spike(스파이크) — 모두 free

### 상점 아이템 30개 (`SHOP_ITEMS`, 라인 768~)
6 카테고리 × 5개: frame(테두리), aura(오라), hat(모자/+15%XP), face(표정/+2코인), pet(펫/+3코인), weapon(무기/+2스타코인)

### 콤보 이미지 시스템 (`COMBO_IMAGE_DATA`)
- 아바타+아이템 합성 이미지를 `avatarId_itemId` 키로 저장
- 현재 5 아바타 × 30 아이템 = 150개 조합 (base64 임베딩)
- `AvatarWithItems` 컴포넌트에서 사용

---

## 오리지널 캐릭터 (전환 대기 중)

### 선생님 캐릭터 (오리지널)
| 이름 | 동물 | 역할 |
|------|------|------|
| 루미 (Lumi) | 여우 | 토론 코치 |
| 미오 (Mio) | 고양이 | 책 도우미 |
| 노아 (Noah) | 부엉이 | 책 추천가 |

### 플레이어 캐릭터 (오리지널) — 10종
대시(치타), 벅스(토끼), 제로(늑대), 너츠(다람쥐), 버디(독수리), 무진(곰), 몽키(원숭이), 아스(사슴), 섀도(표범), 릭스(도마뱀)

### 전환 방법
```bash
./rollback.sh brawl     # 브롤스타즈 버전으로
./rollback.sh original  # 오리지널 캐릭터로
./rollback.sh status    # 현재 상태 확인
```

---

## 앱 주요 기능

### 책 데이터 (`BOOKS` 배열, 라인 341~578)
5권 등록됨:
1. 청소년을 위한 외교광장 (3주차)
2. 씨앗을 부탁해 (2주차)
3. 생각이 크는 인문학: 우주 (1주차)
4. 선생님, 노동이 뭐에요? (4주차)
5. 법의학이야기 (5주차)

각 책에 포함: chapters, summary, keyPoints, characters, discussionTopics(5개), deepTopics(3개), quizzes(5개)

### 게이미피케이션 시스템
- **XP/레벨**: 토론·퀴즈·독서로 XP 획득, 레벨업
- **코인**: 상점에서 아이템 구매
- **일일 미션**: 3개씩 랜덤 출제 (`MISSION_TEMPLATES`)
- **배지**: 활동 기반 자동 해금
- **연속 출석**: 스트릭 보상

### 토론 시스템
- `startDiscussion()` 함수로 토론 시작 (라인 1936~)
- `sanitizeTeacherText(text, firstName)` — 선생님 말투 일관성 보정 함수 (라인 1907~1934)
  - 2인칭 대명사(네가/너는/너의) → 학생 이름으로 자동 치환
  - 존댓말(할까요/나요/건가요) → 반말(할까/니/거야) 자동 변환
  - 받침 감지 `hasBatchim()` → 아/야, 이/가, 은/는 자동 결정
- `getFirstName()` — 성 제거 (김건우 → 건우)
- `generateAIResponse()` — 폴백 응답 (API 실패 시, 반말 통일됨)
- 실제 AI 응답은 Firebase `discussionCoach` 함수 사용

### PWA 설치
- `beforeinstallprompt` 이벤트 감지 → 설치 배너 표시
- Google Play 프로텍트 경고 안내 문구 포함
- `localStorage.bq_install_dismissed`로 중복 표시 방지
- 설치 완료 또는 닫기 시 플래그 저장

### 기타
- 음성 입력/출력 (Web Speech API + Google Cloud TTS)
- 책에게 질문하기 (콜레트 선생님)
- 책 추천 (바이런 선생님 + 알라딘 API)
- 독서 타이머
- 버전 관리/복원 시스템 (`DATA_VERSIONS`, 라인 ~3431)

---

## 나노바나나 프롬프트 문서들

| 파일명 | 내용 |
|--------|------|
| `나노바나나_선생님캐릭터_v2.docx` | 게임풍 선생님 캐릭터 (루미/미오/노아) 9장 |
| `나노바나나_플레이어캐릭터_v2.docx` | 게임풍 플레이어 캐릭터 10종 |
| `나노바나나_상점아이템_프롬프트.docx` | 투명배경 오버레이 아이템 30개 |
| `콤보프롬프트/01~10_*.docx` | 캐릭터×아이템 합성 이미지 300개 (10파일) |
| `나노바나나_오리지널캐릭터_프롬프트.docx` | v1 귀여운 스타일 (v2로 대체됨) |

---

## 진행 예정 작업

1. **300개 콤보 이미지 생성** — 나노바나나 프롬프트 준비 완료, 천천히 생성 진행
2. **오리지널 캐릭터 전환** — 이미지 완성 후 `rollback.sh original` + Firebase 배포
3. **Firebase 배포** — `firebase deploy --only functions` (말투 수정 반영)
4. **GitHub Pages 배포** — index.html 변경사항 push

---

## 배포 명령어

```bash
# Firebase Functions 배포
cd 건우독서앱/functions && npm install && cd .. && firebase deploy --only functions

# GitHub Pages는 저장소에 push하면 자동 배포
# 저장소: yunagunwoo-netizen/bookquest (GitHub)
```

---

## 최근 수정 이력

### 북퀘스트_2 세션 작업 (2026-04, Opus 4.6 → 4.7 인계)

#### 1. 대시(Dash) 캐릭터 추가 — 오리지널 캐릭터 1호 적용
- **배경**: 기존 브롤스타즈 5캐릭터는 콜라보 개념으로 유지 (나중에 브롤스타즈 측 정식 제안 검토), 오리지널 캐릭터를 하나씩 추가하는 방식
- `avatars/dash.png` (200×200) + `avatars/dash_sm.png` (60×60) 생성 (원본 2048×2048 `Dash.png` 리사이즈)
- `AVATAR_DATA`에 `dash(대시)` 추가 — 기존 5캐릭터 뒤에 `// ─── 오리지널 캐릭터 ───` 주석으로 구분
- `COMBO_AVATARS`에 dash 추가
- `getComboImagePath` 함수 확장 — base64 데이터 없으면 `avatars/combos/{avatarId}_{itemId}.png` 외부 파일 폴백 지원
- 새 상수 `EXTERNAL_COMBO_AVATARS` 도입 — 앞으로 오리지널 캐릭터 추가 시 이 배열에 ID만 넣으면 됨

#### 2. 관리자(Admin) 시스템 추가
- **접근**: 프로필 탭 하단 "🔒 관리자 모드" 버튼 → PIN **1234** 입력
- **구성요소**: `AdminPanel` 컴포넌트 + `AdminLoginModal`
- **콘텐츠 관리**: 등록된 책 목록, 상점 아이템, 아바타 현황 조회
- **유저 관리**: 프로필 정보, XP/코인 수동 조정, 독서 진행도 확인, 데이터 초기화
- **앱 설정**: 캐릭터 테마 정보, 앱 정보, 기능 상태 확인
- ⚠️ 작업 중 index.html이 일부 잘리는 사고 발생 → 백업 파일에서 복원 후 재적용 완료

#### 3. 이미지 용량 최적화 (GitHub Pages 1GB 한도 대응)
- **콤보 이미지 리사이즈**: `avatars/combos/` 180개 (6캐릭터 × 30아이템: shelly, nita, leon, crow, spike, dash) 원본 2~10MB → **200×200 PNG**로 일괄 변환 (총 1.1GB → **약 15MB**)
  - 참고: 앱 내 콤보 이미지 최대 렌더 크기는 110px 정도이므로 200px 충분
- **미사용 원본 이미지 22개**: `_원본이미지/` 폴더로 이동 + `.gitignore`에 추가 (132MB 절감)
- **PDF 5개 (294MB)**: `.gitignore`에 `*.pdf` 추가
- **`오리지날 캐릭터/` 폴더**: `.gitignore`에 추가 (원본 2048px 캐릭터 이미지 제외)
- **최종 결과**: 1.3GB+ → **약 46MB (748개 파일)** 로 정리 완료, push 가능 상태

#### 4. 다음 세션(Opus 4.7)에서 이어서 할 작업 후보
- [ ] GitHub Pages에 실제로 `git add . && git commit && git push` 실행하여 배포 확인
- [ ] 대시 캐릭터 실기기/브라우저에서 아이템 장착 콤보 이미지 렌더링 검증
- [ ] 관리자 모드 각 탭 동작 QA (PIN 1234 로그인, 유저 데이터 초기화 등)
- [ ] 나머지 오리지널 캐릭터 순차 추가 (벅스, 제로, 너츠, 버디, 무진, 몽키, 아스, 섀도, 릭스)
  - 콤보 이미지 30장씩 생성 → `avatars/combos/`에 `{avatarId}_{itemId}.png` 형식으로 저장
  - `AVATAR_DATA` + `COMBO_AVATARS`에 ID 추가 (자동으로 외부 파일 경로 사용)
- [ ] 10캐릭터 모두 추가 완료 시 선생님 캐릭터(루미/미오/노아)까지 전환 → `rollback.sh original` 실행 검토

---

### 말투 버그 수정
- `sanitizeTeacherText()` 함수 도입 — 토론 주제/힌트에 자동 적용
- `hasBatchim()` + `getFirstName()` 유틸리티 추가
- "건우의 생각을 말해 봐!" → "건우야, 생각을 말해 봐!" (받침 기반 아/야)
- "네가" → "건우가", "너는" → "건우는" 자동 치환
- 5권 전체 discussionTopics/deepTopics 존댓말→반말 수정
- `generateAIResponse` 폴백 응답도 반말 통일
- AI 서비스 에러 폴백 메시지도 반말 통일

### PWA 설치 배너 개선 (최신)
- 설치 완료 시에도 `bq_install_dismissed` 플래그 저장
- Google Play 프로텍트 "안전하지 않은 앱" 경고 안내 문구 추가

### 캐릭터 시스템
- 오리지널 캐릭터 디자인 완료 (나노바나나 v2 프롬프트)
- 롤백 시스템 구현 (rollback.sh)
- 현재 브롤스타즈 버전 활성화 상태

### 사업계획서
- `BookQuest_사업계획서.docx` — 11개 섹션 완성 (캐릭터 IP 전략 포함)
