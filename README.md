# academic-humanizer-kr

한국어 **학술 논문** 텍스트에서 'AI가 쓴 티'를 제거하되, **헤징·명사화·인용·IMRaD 같은
정당한 학술 규범은 보존**하는 Claude Code 하네스(플러그인).

> 의미·수치·고유명사·인용은 **한 글자도 건드리지 않는다.** 없는 인용은 만들지 않고
> 플래그만 한다.

[epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai)(범용 한국어 휴머나이저)에서
영감을 받되, **학술 레지스터에 맞게 taxonomy를 재조정**한 것이 핵심 차별점이다.

## 왜 별도 하네스인가 — "제거가 아니라 재조정"

범용 휴머나이저는 헤징·명사화·형식구조를 모두 'AI 티'로 보고 깎는다. 그러나 **학술 글에서는
그것들이 규범**이다.

| 요소 | 범용 휴머나이저 | 이 하네스 (`--academic`) |
|------|----------------|--------------------------|
| 단일 헤징("~로 보인다") | 제거 | **보존** (학술성의 표지) |
| 분야 표준 명사화("타당성") | 동사화 | **보존** |
| 객관성 피동("측정되었다") | 능동화 | **보존** |
| IMRaD·형식 구조 | 산문화 | **보존** |
| 인용 | 최소화 | **불가침** + 환각은 플래그 |
| 공허 메타·Hype·번역투·리듬 균일 | 제거 | **제거**(동일) |

이 경계선은 다중 소스 연구(Manchester Academic Phrasebank, GMU Writing Center, 서울대·
경희대 글쓰기센터, Editage, MDPI 교수 인식 연구, ResearchLeap VERMILLION framework)에
근거한다 → `skills/humanize-academic/references/research-basis.md`.

## 무엇을 잡는가 (11범주)

1. 공허한 메타·상투구 (S1) · 2. 근거 없는 일반화 (S1→플래그) · 3. 환각 인용 (S1→플래그만)
· 4. 헤징 오용 (중첩만 교정) · 5. 명사화 (행위자 은폐 연쇄만 해체) · 6. 번역투 (S1/S2)
· 7. 리듬·구조 균일성 · 8. 접속사·전이 공식 · 9. Hype·주관 형용사 (S1) · 10. 시각·서식 장식
· 11. 피동 (기계적 일변도만 일부 능동화)

전체: `skills/humanize-academic/references/academic-tell-taxonomy.md`

## 사용법

### 자연어
- "이 논문 서론 AI 티 없애줘"
- "초록 사람이 쓴 것처럼 다듬어줘"
- "학위논문 3장 문장 자연스럽게"

### 슬래시 커맨드
```
/humanize-academic <텍스트 또는 파일경로>
/humanize-academic draft.md --strict     # 5단계 파이프라인
/humanize-academic essay.md --general    # 비학술 모드(공격적)
```

## 모드

- **`--academic` (기본):** 학술 규범 보존. 논문·학위논문·초록·학술지 원고.
- **`--general`:** 에세이·블로그. 헤징·명사화·형식까지 공격적 다듬음.
- **Fast (≤5,000자):** 단일 에이전트 1패스 (~2–3분).
- **Strict (≥8,000자 또는 `--strict`):** 탐지→교정→충실도감사+자연성리뷰, 최대 3루프.

## 4대 불변 원칙

1. **의미 불변** — 사실·수치·고유명사·인용·수식 한 글자도 안 바꿈.
2. **인용 날조 절대 금지** — 근거 없는 일반화·환각 인용은 `[저자 확인: …]` 플래그만.
3. **학술 규범 보존** — 단일 헤징·표준 명사화·객관성 피동·IMRaD는 건드리지 않음.
4. **과교정 방지** — 변경률 30% 경고, 50% 중단.

## 윤리

목적은 **한국어 학술 글쓰기 품질 향상**이지 AI 탐지 회피·학술 부정이 아니다. 표절 검사·
연구 진실성 검증을 대체하지 않으며, **인용·데이터·주장은 저자가 책임진다.**

## 구성

```
academic-humanizer-kr/
├── .claude-plugin/{plugin.json, marketplace.json}
├── skills/humanize-academic/
│   ├── SKILL.md
│   └── references/{academic-tell-taxonomy, academic-norms-keep, quick-rules, research-basis}.md
├── agents/{academic-humanize-monolith, academic-tell-detector, academic-style-rewriter,
│           scholarly-fidelity-auditor, academic-naturalness-reviewer}.md
└── commands/humanize-academic.md
```

설치: [INSTALL.md](INSTALL.md). 라이선스: Apache-2.0.
