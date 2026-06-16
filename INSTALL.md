# 설치 가이드

## 방법 1 — 로컬 마켓플레이스 (개발/단독 사용)

Claude Code에서:
```
/plugin marketplace add C:\Users\user\academic-humanizer-kr
/plugin install academic-humanizer-kr@academic-humanizer-kr
```
이미 `.claude-plugin/marketplace.json`이 포함되어 있으므로 이 폴더 자체가 마켓플레이스다.

## 방법 2 — GitHub 마켓플레이스 (게시 후)

```
/plugin marketplace add howtoconsulting5776-boop/academic-humanizer-kr
/plugin install academic-humanizer-kr@academic-humanizer-kr
```

## 방법 3 — 수동 링크

플러그인 폴더를 Claude Code가 인식하는 위치에 두거나, 스킬·에이전트·커맨드를
`~/.claude/`의 해당 디렉터리로 복사한다.

## 확인

설치 후:
```
/humanize-academic 이 문장은 매우 중요한 의미를 가지며 시사하는 바가 크다고 할 수 있다.
```
→ 공허 메타·Hype가 교정되고 메트릭·등급이 출력되면 정상.

## 요구 사항

- Claude Code (스킬·서브에이전트·슬래시커맨드 지원 버전)
- 외부 의존성 없음 (순수 프롬프트 하네스). 모델은 opus 권장(에이전트 frontmatter 기본값).

## 업데이트

GitHub 게시본은 `/plugin marketplace update` 후 재설치. 로컬은 파일을 직접 수정하면 즉시 반영.
