# tests — 불변원칙 회귀 스위트

이 하네스는 LLM 프롬프트 기반이라 출력이 비결정적이다. 그러나 **4대 불변원칙은
기계적으로 검증 가능한 불변식**이다. 이 스위트는 그 불변식을 사람 눈이 아니라 **코드로
강제**한다(math-harness의 "틀린 풀이 차단" 철학과 동일).

## 실행

```bash
python tests/run_tests.py        # 종료코드 0=통과, 1=실패
python tests/preservation_lint.py # 린터 자가 데모
```

외부 의존성 없음(표준 라이브러리만). CI: `.github/workflows/smoke.yml`가 push/PR마다 실행.

## 무엇을 강제하는가

`preservation_lint.lint(original, output, mode, keep_hedges)`가 (원문, 출력)을 대조해
위반을 결정론적으로 잡는다:

| 코드 | 강제하는 불변원칙 |
|------|-------------------|
| `NUMBER_DRIFT` / `NUMBER_INVENTED` | ①의미 불변 — 표본수·p값·통계 보존 |
| `CITATION_FABRICATION` | ②인용 날조 금지 — 출력 인용 ⊆ 원문 인용 (**가장 중요**) |
| `CITATION_DROPPED` | ①의미 불변 — 실제 인용 보존 |
| `QUOTE_ALTERED` | ①의미 불변 — 직접인용 글자 단위 보존 |
| `HEDGE_STRIPPED` | ③학술 규범 보존 — academic 모드에서 단일 헤징 보존 |
| `OVER_EDIT` | ④과교정 방지 — 변경률 ≤50% |

## 케이스 구조 (`cases.json`)

각 케이스는 (원문, **good** 출력, **bad** 출력, 기대 위반코드)의 골든 트리플이다.
러너는 두 가지를 단언한다:
1. `good`은 위반 0건으로 통과 — 정상 휴머나이즈를 오탐하지 않는다.
2. `bad`는 `expect_bad`의 코드를 모두 잡는다 — 불변원칙을 실제로 강제한다.

핵심 케이스:
- `02-citation-fabrication` — "많은 연구가~"를 인용 *날조*로 채우면 차단(플래그는 통과).
- `04-keep-single-hedge` — "이어질 수 있다"를 단정화하면 academic에서 차단.
- `05-general-mode` — 같은 단정화가 general 모드에선 허용(모드 분기 검증).
- `08-clean-text` — 깨끗한 문장에 인용을 덧대면 차단(과교정 방지).

## 새 케이스 추가

`cases.json`에 객체 하나 추가하면 끝. 새 불변식이 필요하면 `preservation_lint.py`에
검사 함수와 위반코드를 더하고, 그 코드를 잡는 케이스를 넣는다.
