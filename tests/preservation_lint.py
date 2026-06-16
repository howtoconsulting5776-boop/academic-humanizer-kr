"""
preservation_lint.py — academic-humanizer-kr 불변원칙 검사기 (deterministic)

이 하네스는 LLM 프롬프트 하네스라 출력이 비결정적이다. 그러나 4대 불변원칙은
*기계적으로 검증 가능한 불변식*이다. 이 모듈은 (원문, 휴머나이즈된 출력)을 받아
다음을 위반하는지 결정론적으로 검사한다:

  1. 의미 불변      → 숫자·통계·연도·직접인용이 그대로 보존되는가
  2. 인용 날조 금지  → 출력에 원문에 없던 인용이 새로 생기지 않았는가 (가장 중요)
  3. 학술 규범 보존  → (academic 모드) 보존 대상 단일 헤징이 단정으로 깎이지 않았는가
  4. 과교정 방지     → 변경률이 50%를 넘지 않는가

run_tests.py가 골든 케이스(원문, 좋은출력, 나쁜출력)에 이 린터를 돌려, '좋은출력'은
통과하고 '나쁜출력'은 기대한 위반코드를 잡아내는지 단언한다. 외부 의존성 없음(표준 라이브러리).
"""

from __future__ import annotations
import re
import difflib
from dataclasses import dataclass, field


# ── 위반 코드 ───────────────────────────────────────────────────────────────
NUMBER_DRIFT = "NUMBER_DRIFT"            # 원문 숫자/통계가 사라지거나 변형됨
NUMBER_INVENTED = "NUMBER_INVENTED"      # 출력에 없던 숫자가 새로 생김
CITATION_FABRICATION = "CITATION_FABRICATION"  # 출력에 원문에 없던 인용이 생김 (날조)
CITATION_DROPPED = "CITATION_DROPPED"    # 원문의 실제 인용이 사라짐
QUOTE_ALTERED = "QUOTE_ALTERED"          # 직접인용("...") 내용이 바뀜
HEDGE_STRIPPED = "HEDGE_STRIPPED"        # (academic) 보존해야 할 단일 헤징이 제거됨
OVER_EDIT = "OVER_EDIT"                  # 변경률 50% 초과


# ── 추출기 ─────────────────────────────────────────────────────────────────
# 인용 패턴: (저자, 2020) / (Smith, 2020) / 홍길동(2020) / Smith (2020) / (홍길동, 2020a)
_CIT_PATTERNS = [
    re.compile(r"\(([^()]*?\d{4}[a-z]?)\)"),                  # (… 2020) 괄호형
    re.compile(r"([가-힣]{2,5})\s*\(\s*(\d{4}[a-z]?)\s*\)"),   # 홍길동(2020) 한글 서술형
    re.compile(r"\b([A-Z][A-Za-z\-]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][A-Za-z\-]+)?)\s*\(\s*(\d{4}[a-z]?)\s*\)"),  # Smith (2020)
]

# 숫자/통계: 백분율, p값, 소수, 정수 (연도 포함)
_NUM_PATTERN = re.compile(r"\d+(?:[.,]\d+)*\s*%?")

# 직접인용: 큰따옴표/낫표 안의 내용
_QUOTE_PATTERN = re.compile(r"[\"“]([^\"”]{1,400})[\"”]|「([^」]{1,400})」")


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s).strip()


def extract_numbers(text: str) -> list[str]:
    """통계·연도·수치 토큰을 정규화해 멀티셋으로 반환."""
    return sorted(_norm(m.group(0)) for m in _NUM_PATTERN.finditer(text))


def extract_citations(text: str) -> set[str]:
    """인용 (저자+연도) 시그니처 집합. 형식 차이는 정규화로 흡수."""
    cites: set[str] = set()
    for pat in _CIT_PATTERNS:
        for m in pat.finditer(text):
            # 연도만 키로 쓰지 않고 (앞부분 일부 + 연도)로 시그니처화
            groups = [g for g in m.groups() if g]
            sig = _norm("".join(groups))
            # 연도 추출
            ym = re.search(r"\d{4}", sig)
            if ym:
                # 저자 토큰(연도 앞 한글/영문 일부) + 연도
                author = _norm(re.sub(r"\d{4}[a-z]?", "", sig))[:8]
                cites.add(f"{author}|{ym.group(0)}")
    return cites


def extract_quotes(text: str) -> list[str]:
    """직접인용 내용(정규화) 리스트."""
    out = []
    for m in _QUOTE_PATTERN.finditer(text):
        content = m.group(1) or m.group(2) or ""
        if content:
            out.append(_norm(content))
    return sorted(out)


def change_rate(original: str, output: str) -> float:
    """문자 단위 변경률 (0~1). difflib 유사도의 보수."""
    a, b = _norm(original), _norm(output)
    if not a:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    return round(1.0 - ratio, 4)


# ── 메인 린터 ──────────────────────────────────────────────────────────────
@dataclass
class LintResult:
    violations: list[dict] = field(default_factory=list)
    change_rate: float = 0.0

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0

    def codes(self) -> set[str]:
        return {v["code"] for v in self.violations}

    def add(self, code: str, detail: str):
        self.violations.append({"code": code, "detail": detail})


def lint(original: str, output: str, mode: str = "academic",
         keep_hedges: list[str] | None = None,
         max_change_rate: float = 0.50) -> LintResult:
    """원문 대비 출력의 불변원칙 위반을 검사."""
    res = LintResult()
    res.change_rate = change_rate(original, output)

    # 1. 의미 불변 — 숫자/통계 보존
    o_nums, h_nums = extract_numbers(original), extract_numbers(output)
    for n in set(o_nums):
        if o_nums.count(n) > h_nums.count(n):
            res.add(NUMBER_DRIFT, f"원문 수치 '{n}' 가 출력에서 사라지거나 변형됨")
    for n in set(h_nums):
        if h_nums.count(n) > o_nums.count(n):
            res.add(NUMBER_INVENTED, f"출력에 없던 수치 '{n}' 가 새로 생김")

    # 2. 인용 날조 금지 (가장 중요) — 출력 인용 ⊆ 원문 인용
    o_cit, h_cit = extract_citations(original), extract_citations(output)
    for c in h_cit - o_cit:
        res.add(CITATION_FABRICATION, f"원문에 없던 인용이 출력에 생성됨: {c}")
    for c in o_cit - h_cit:
        res.add(CITATION_DROPPED, f"원문의 실제 인용이 출력에서 사라짐: {c}")

    # 1b. 직접인용 보존
    o_q, h_q = extract_quotes(original), extract_quotes(output)
    # 원문 직접인용은 모두 출력에 그대로 있어야 함
    for q in o_q:
        if q not in h_q:
            res.add(QUOTE_ALTERED, f"직접인용 내용이 변경/삭제됨: \"{q[:30]}…\"")

    # 3. 학술 규범 보존 (academic 모드) — 지정된 단일 헤징이 보존되어야 함
    if mode == "academic" and keep_hedges:
        for hedge in keep_hedges:
            if _norm(hedge) in _norm(original) and _norm(hedge) not in _norm(output):
                res.add(HEDGE_STRIPPED,
                        f"보존 대상 단일 헤징 '{hedge}' 가 academic 모드에서 제거됨")

    # 4. 과교정 방지
    if res.change_rate > max_change_rate:
        res.add(OVER_EDIT, f"변경률 {res.change_rate:.0%} > {max_change_rate:.0%} 한계")

    return res


if __name__ == "__main__":
    # 간단 자가 데모
    orig = '본 연구는 32명을 대상으로 했다. 효과는 유의했다(p < .05). 학습이 효과적일 수 있다.'
    good = '본 연구는 32명을 대상으로 분석했다. 효과는 유의했다(p < .05). 학습이 효과적일 수 있다.'
    bad = '본 연구는 40명을 분석했다(Kim, 2021). 학습은 효과적이다.'
    print("GOOD:", lint(orig, good, keep_hedges=["효과적일 수 있다"]).codes() or "PASS")
    print("BAD :", sorted(lint(orig, bad, keep_hedges=["효과적일 수 있다"]).codes()))
