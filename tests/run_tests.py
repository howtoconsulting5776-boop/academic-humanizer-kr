#!/usr/bin/env python3
"""
run_tests.py — academic-humanizer-kr 회귀 스위트 러너 (외부 의존성 없음)

각 골든 케이스에 preservation_lint를 돌려 두 가지를 단언한다:
  - good 출력은 위반 0건으로 통과해야 한다 (정상 휴머나이즈를 오탐하지 않음)
  - bad 출력은 expect_bad의 위반 코드를 *모두* 잡아내야 한다 (불변원칙을 코드로 강제)

이로써 "정당한 헤징을 깎지 않고 / 인용을 날조하지 않고 / 수치를 보존한다"는 철칙이
사람 눈이 아니라 테스트로 강제된다. pytest 없이 `python tests/run_tests.py`로 실행.
종료코드: 모두 통과 0, 하나라도 실패 1.
"""
from __future__ import annotations
import json
import os
import sys

# Windows 콘솔(cp949)에서도 한글이 깨지지 않게 UTF-8 출력 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preservation_lint import lint  # noqa: E402

CASES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases.json")


def run() -> int:
    with open(CASES, encoding="utf-8") as f:
        cases = json.load(f)

    passed = failed = 0
    for c in cases:
        cid = c["id"]
        mode = c.get("mode", "academic")
        keep = c.get("keep_hedges")

        # (1) good 은 깨끗해야 한다
        g = lint(c["original"], c["good"], mode=mode, keep_hedges=keep)
        if g.passed:
            print(f"  PASS  {cid} :: good 통과 (변경률 {g.change_rate:.0%})")
            passed += 1
        else:
            print(f"  FAIL  {cid} :: good 가 위반을 일으킴 → {sorted(g.codes())}")
            for v in g.violations:
                print(f"        - {v['code']}: {v['detail']}")
            failed += 1

        # (2) bad 는 기대한 위반을 모두 잡아야 한다
        b = lint(c["original"], c["bad"], mode=mode, keep_hedges=keep)
        expected = set(c.get("expect_bad", []))
        got = b.codes()
        if expected and expected.issubset(got):
            print(f"  PASS  {cid} :: bad 차단 {sorted(expected & got)}")
            passed += 1
        else:
            print(f"  FAIL  {cid} :: bad 가 기대 위반을 못 잡음. 기대 {sorted(expected)} / 실제 {sorted(got)}")
            failed += 1

    total = passed + failed
    print("\n" + "=" * 60)
    print(f"  결과: {passed}/{total} 통과, {failed} 실패")
    print("=" * 60)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
