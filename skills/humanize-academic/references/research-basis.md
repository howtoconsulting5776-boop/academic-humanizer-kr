# 연구 근거 종합 (Research Basis)

이 taxonomy는 2026-06-16 수행한 다중 소스 웹 리서치에 근거한다. 핵심 통찰은
**"AI 슬롭 vs 정당한 학술 규범"의 경계선**이며, 이것이 범용 휴머나이저와 이 하네스를
가른다.

## 축 1 — 좋은 학술적 글쓰기의 보편 원칙
- **명료성·통일성·유기성·간결성** (서울대 온라인 글쓰기교실): 주어-서술어 호응, 단락
  소주제-뒷받침 일관, 문장 간 논리적 결합, "잘 쓰인 논문은 간결하다."
- **문장 규칙** (경희대 글쓰기센터): 50자 초과 문장 지양("네 줄 넘긴 문장은 나쁜 문장"),
  추측성 "~인 것 같다" 회피, 수식어-피수식어 거리 최소화, 구체적 주어 사용, 의미 중복 제거.
- **6대 실전 조언** (Editage): ① ‑tion/명사화 제거("carried out an exploration"→"explored"),
  ② 축약·구어체 금지, ③ 정확한 전문용어, ④ 객관적 어조(주관 형용사 회피, 객관성 피동 선호),
  ⑤ **적절한 헤징 — 단 과도한 헤징은 문장을 약화**, ⑥ IMRaD 논리 구성.
- **헤징은 규범** (Manchester Academic Phrasebank; GMU Writing Center): 절대 확실성 회피와
  과잉일반화 회피가 학술 문체의 핵심. 양태(may<might<could … will probably). 단,
  무자격 단정은 신뢰를 깎으므로 적정 헤징은 *유지*하되 중첩은 피한다.

## 축 2 — 한국어 학술 문체 규범
- 학위논문 작성 지침(한국외대·고려대·이화여대): 형식·인용·각주·참고문헌 규범 준수.
- '~다' 평서체 일관, 명사화·피동의 적정선, 번역투 회피(한국 번역학계 계보: 이영옥~김혜영).
- 번역투가 한국어 AI 텍스트의 가장 결정적 시그니처 — im-not-ai A 범주를 학술에도 계승.

## 축 3 — 사람 vs AI 학술 텍스트 구분 마커
- **MDPI(2025), 대학교수 관점:** 반복 문장 구조, "It is important to note" 반복,
  동일 문두("Another example is…"), 5단락 정형, 고정 간격 전이어, 균일 단락 형태.
- **ResearchLeap VERMILLION framework:** 대명사 모호("their efforts"), 균일 절 길이,
  template 패턴("An analysis of…", "The findings suggest…"), 전이 상투구(Moreover/
  Furthermore/In conclusion), em-dash 남용, 양태 남용, 단락 3~5줄 고정, lexical inflation
  (추상 명사 cascade가 행위자·증거사슬을 은폐), **인간 글의 부재 요소**: 개인 목소리·
  구체 사례·idiosyncrasy.
- **검색 종합:** AI는 논쟁적 주제를 합의로 평탄화, "X have been described as Y"를 누가·왜
  없이 단정, 환각 인용 위험.
- **반례 주의:** 학술 글로 쓰인 AI 텍스트는 본래 객관·격식·집중되어 있어 탐지가 더 어렵다
  (arXiv 2306.05524). 그래서 *학술 특화* 마커(공허 메타·무출처 일반화·중첩 헤징·리듬
  균일성)가 범용 마커보다 신뢰도 높다.

## 축 4 — 교정 전략 (반영)
- 평가어 → 증거 치환, 메타 서두 삭제, 중첩 헤징만 1중으로, 연쇄 명사화만 동사구로,
  번역투 직역 환원, 리듬·전이 변주. **근거 없는 내용은 생성 금지 — 플래그만.**

## 설계 결론 (양면 범주의 근거)
헤징(4)·명사화(5)·피동(11)·형식구조는 학술 규범이므로 **two-sided**로 처리:
*중첩/은폐/기계적 일변도*만 슬롭으로 교정하고, *단일/표준/객관성* 용법은 보존한다.
이 경계가 `academic-norms-keep.md` 화이트리스트로 코드화되었다.

## 출처 (markdown)
- [서울대 온라인 글쓰기교실 — 논문 쓰기](https://owl.snu.ac.kr/2465/)
- [경희대 글쓰기센터 — 문장 쉽게 잘 쓰는 법](https://khwriting.khu.ac.kr/writer/basic02.php)
- [Editage — 학술적 글쓰기 향상 6가지](https://www.editage.co.kr/insights/6-actionable-tips-to-improve-academic-writing-0)
- [Manchester Academic Phrasebank — Being cautious](https://www.phrasebank.manchester.ac.uk/using-cautious-language/)
- [GMU Writing Center — Hedges: Softening Claims](https://writingcenter.gmu.edu/writing-resources/research-based-writing/hedges-softening-claims-in-academic-writing)
- [MDPI — Key Features to Distinguish Human- and AI-Generated Texts (Professors)](https://www.mdpi.com/3042-8130/2/1/2)
- [ResearchLeap — The Disappearing Author (VERMILLION)](https://researchleap.com/the-disappearing-author-linguistic-and-cognitive-markers-of-ai-generated-communication/)
- [arXiv 2306.05524 — Detectability of ChatGPT Content in Academic Writing](https://arxiv.org/pdf/2306.05524)
- 모태: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (범용 한국어 휴머나이저, MIT)
