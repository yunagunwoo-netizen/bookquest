# BookQuest 버전 관리 스킬 (매 작업 시 자동 실행)

이 문서는 Claude (및 개발자) 가 매 배포 전에 반드시 따라야 하는 버전 관리 규칙이다.

## 언제 실행하는가

**매번 index.html 을 수정한 후, 배포 전에 반드시 실행한다.**

- 기능 추가 / 버그 수정 / UI 변경 중 하나라도 있으면 실행
- "배포해줘", "firebase deploy" 같은 요청을 받기 전에 먼저 실행
- 사용자가 명시적으로 "버전 안 올려도 돼" 라고 하면 건너뜀

## 버전 넘버링 규칙 (SemVer)

- **PATCH (1.2.0 → 1.2.1)**: 버그 수정, 자잘한 UI 조정
- **MINOR (1.2.0 → 1.3.0)**: 새 기능 추가, 의미 있는 개선
- **MAJOR (1.2.0 → 2.0.0)**: 대규모 리팩토링, 파괴적 변경

기본 MINOR 올림. 단순 버그픽스만 있으면 PATCH.

## 실행 방법

```bash
cd C:\dev\bookquest
python scripts/bump_version.py --version "1.3.0" --title "이번 버전 제목" --changes "변경1" "변경2" "변경3"
```

## 변경사항 작성 가이드

한 항목당 한 줄, 한국어, 사용자 관점.

❌ "useEffect 수정", "리팩토링"
✅ "아바타 AI 토론 배틀 추가", "관리자 모드 배틀 무제한"

## 스크립트가 자동으로 하는 일

1. 현재 `APP_VERSION` 파악
2. 현재 `index.html` → `backup/index_v{기존}.html` 복사
3. `APP_VERSION`, `APP_BUILD_DATE` 갱신
4. `CHANGELOG` 최상단에 새 항목 추가
5. `VERSION_HISTORY` 에서 이전 버전을 backup 경로로 강등
6. `VERSION_HISTORY` 최상단에 새 버전 추가

## 표준 작업 순서

1. 코드 수정 완료
2. `python scripts/bump_version.py ...` 실행
3. `firebase deploy --only hosting`
4. 사용자에게 URL 안내

**반드시 이 순서 유지.** 배포 후 버전 올리면 앱 안 업데이트 노트가 최신 변경과 어긋난다.
