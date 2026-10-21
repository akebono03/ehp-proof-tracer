# Phase 166 R3-AO 型・次元の意味的監査

## Summary

```json
{
  "phase": "166-r3ao-semantic-type-audit",
  "count": 112,
  "source_counts": {
    "simple": 28,
    "structured": 61,
    "zero": 23
  },
  "status_counts": {
    "partially_verified": 28,
    "pass": 84
  },
  "issue_counts": {},
  "production_code_modified": false,
  "proof_search_executed": false,
  "scope": "group orders, generator degree, composition interfaces and Element-ID stems; simple-name identity not fully verified"
}
```

## 各群

### n=2 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}`

検出事項: なし

- ι2: Element=[1], source=2, target=2, issues=[]

### n=2 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}`

検出事項: なし

- η2: Element=[2], source=3, target=2, issues=[]

### n=2 k=2 — pass

取得経路: structured

TeX: `\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}`

検出事項: なし

- η2^2: Element=[2, 2], source=4, target=2, issues=[]

### n=2 k=3 — pass

取得経路: structured

TeX: `\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}`

検出事項: なし

- η2^3: Element=[2, 2, 2], source=5, target=2, issues=[]

### n=2 k=4 — pass

取得経路: structured

TeX: `\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}`

検出事項: なし

- η2ν': Element=[2, 3], source=6, target=2, issues=[]

### n=2 k=5 — pass

取得経路: structured

TeX: `\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}`

検出事項: なし

- η2ν'η6: Element=[2, 3, 2], source=7, target=2, issues=[]

### n=2 k=6 — pass

取得経路: structured

TeX: `\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}`

検出事項: なし

- η2ν'η6^2: Element=[2, 3, 2, 2], source=8, target=2, issues=[]

### n=2 k=7 — pass

取得経路: zero

TeX: `\pi_{9}^{2} = 0`

検出事項: なし


### n=3 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}`

検出事項: なし

- ι3: Element=[1], source=3, target=3, issues=[]

### n=3 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}`

検出事項: なし

- η3: Element=[2], source=4, target=3, issues=[]

### n=3 k=2 — pass

取得経路: structured

TeX: `\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}`

検出事項: なし

- η3^2: Element=[2, 2], source=5, target=3, issues=[]

### n=3 k=3 — pass

取得経路: structured

TeX: `\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}`

検出事項: なし

- ν': Element=[3], source=6, target=3, issues=[]

### n=3 k=4 — pass

取得経路: structured

TeX: `\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}`

検出事項: なし

- ν'η6: Element=[3, 2], source=7, target=3, issues=[]

### n=3 k=5 — pass

取得経路: structured

TeX: `\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}`

検出事項: なし

- ν'η6^2: Element=[3, 2, 2], source=8, target=3, issues=[]

### n=3 k=6 — pass

取得経路: zero

TeX: `\pi_{9}^{3} = 0`

検出事項: なし


### n=3 k=7 — pass

取得経路: zero

TeX: `\pi_{10}^{3} = 0`

検出事項: なし


### n=4 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{4}^{4} = \mathbb{Z}\{\iota_{4}\}`

検出事項: なし

- ι2: Element=[1], source=4, target=4, issues=[]

### n=4 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}`

検出事項: なし

- η4: Element=[2], source=5, target=4, issues=[]

### n=4 k=2 — pass

取得経路: structured

TeX: `\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=6, target=4, issues=[]

### n=4 k=3 — pass

取得経路: structured

TeX: `\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}`

検出事項: なし

- ν4: Element=[4], source=7, target=4, issues=[]
- E ν': Element=[3], source=7, target=4, issues=[]

### n=4 k=4 — pass

取得経路: structured

TeX: `\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}`

検出事項: なし

- ν4η7: Element=[4, 2], source=8, target=4, issues=[]
- E ν'η7: Element=[3, 2], source=8, target=4, issues=[]

### n=4 k=5 — pass

取得経路: structured

TeX: `\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}`

検出事項: なし

- ν4η7^2: Element=[4, 2, 2], source=9, target=4, issues=[]
- E ν'η7^2: Element=[3, 2, 2], source=9, target=4, issues=[]

### n=4 k=6 — pass

取得経路: structured

TeX: `\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}^{2}\}`

検出事項: なし

- ν4^2: Element=[4, 4], source=10, target=4, issues=[]

### n=4 k=7 — pass

取得経路: zero

TeX: `\pi_{11}^{4} = 0`

検出事項: なし


### n=5 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}`

検出事項: なし

- ι5: Element=[1], source=5, target=5, issues=[]

### n=5 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}`

検出事項: なし

- η5: Element=[2], source=6, target=5, issues=[]

### n=5 k=2 — pass

取得経路: structured

TeX: `\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}`

検出事項: なし

- η5^2: Element=[2, 2], source=7, target=5, issues=[]

### n=5 k=3 — pass

取得経路: structured

TeX: `\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}`

検出事項: なし

- ν5: Element=[4], source=8, target=5, issues=[]

### n=5 k=4 — pass

取得経路: structured

TeX: `\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}`

検出事項: なし

- ν5η8: Element=[4, 2], source=9, target=5, issues=[]

### n=5 k=5 — pass

取得経路: structured

TeX: `\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}`

検出事項: なし

- ν5η8^2: Element=[4, 2, 2], source=10, target=5, issues=[]

### n=5 k=6 — pass

取得経路: structured

TeX: `\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}^{2}\}`

検出事項: なし

- ν5^2: Element=[4, 4], source=11, target=5, issues=[]

### n=5 k=7 — pass

取得経路: structured

TeX: `\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}`

検出事項: なし

- σ''': Element=[6], source=12, target=5, issues=[]

### n=6 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{6}^{6} = \mathbb{Z}\{\iota_{6}\}`

検出事項: なし

- ι2: Element=[1], source=6, target=6, issues=[]

### n=6 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{7}^{6} = \mathbb{Z}/2\{\eta_{6}\}`

検出事項: なし

- η3: Element=[2], source=7, target=6, issues=[]

### n=6 k=2 — pass

取得経路: structured

TeX: `\pi_{8}^{6} = \mathbb{Z}/2\{\eta_{6}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=8, target=6, issues=[]

### n=6 k=3 — pass

取得経路: structured

TeX: `\pi_{9}^{6} = \mathbb{Z}/8\{\nu_{6}\}`

検出事項: なし

- ν6: Element=[4], source=9, target=6, issues=[]

### n=6 k=4 — pass

取得経路: zero

TeX: `\pi_{10}^{6} = 0`

検出事項: なし


### n=6 k=5 — pass

取得経路: structured

TeX: `\pi_{11}^{6} = \mathbb{Z}\{\Delta(\iota13)\}`

検出事項: なし

- \Delta(ι13): Element=[5], source=11, target=6, issues=[]

### n=6 k=6 — pass

取得経路: structured

TeX: `\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}^{2}\}`

検出事項: なし

- ν6^2: Element=[4, 4], source=12, target=6, issues=[]

### n=6 k=7 — pass

取得経路: structured

TeX: `\pi_{13}^{6} = \mathbb{Z}/4\{\sigma''\}`

検出事項: なし

- σ'': Element=[7], source=13, target=6, issues=[]

### n=7 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{7}^{7} = \mathbb{Z}\{\iota_{7}\}`

検出事項: なし

- ι7: Element=[1], source=7, target=7, issues=[]

### n=7 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{8}^{7} = \mathbb{Z}/2\{\eta_{7}\}`

検出事項: なし

- η7: Element=[2], source=8, target=7, issues=[]

### n=7 k=2 — pass

取得経路: structured

TeX: `\pi_{9}^{7} = \mathbb{Z}/2\{\eta_{7}^{2}\}`

検出事項: なし

- η7^2: Element=[2, 2], source=9, target=7, issues=[]

### n=7 k=3 — pass

取得経路: structured

TeX: `\pi_{10}^{7} = \mathbb{Z}/8\{\nu_{7}\}`

検出事項: なし

- ν7: Element=[4], source=10, target=7, issues=[]

### n=7 k=4 — pass

取得経路: zero

TeX: `\pi_{11}^{7} = 0`

検出事項: なし


### n=7 k=5 — pass

取得経路: zero

TeX: `\pi_{12}^{7} = 0`

検出事項: なし


### n=7 k=6 — pass

取得経路: structured

TeX: `\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}^{2}\}`

検出事項: なし

- ν7^2: Element=[4, 4], source=13, target=7, issues=[]

### n=7 k=7 — pass

取得経路: structured

TeX: `\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}`

検出事項: なし

- σ': Element=[8], source=14, target=7, issues=[]

### n=8 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{8}^{8} = \mathbb{Z}\{\iota_{8}\}`

検出事項: なし

- ι2: Element=[1], source=8, target=8, issues=[]

### n=8 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{9}^{8} = \mathbb{Z}/2\{\eta_{8}\}`

検出事項: なし

- η3: Element=[2], source=9, target=8, issues=[]

### n=8 k=2 — pass

取得経路: structured

TeX: `\pi_{10}^{8} = \mathbb{Z}/2\{\eta_{8}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=10, target=8, issues=[]

### n=8 k=3 — pass

取得経路: structured

TeX: `\pi_{11}^{8} = \mathbb{Z}/8\{\nu_{8}\}`

検出事項: なし

- ν5: Element=[4], source=11, target=8, issues=[]

### n=8 k=4 — pass

取得経路: zero

TeX: `\pi_{12}^{8} = 0`

検出事項: なし


### n=8 k=5 — pass

取得経路: zero

TeX: `\pi_{13}^{8} = 0`

検出事項: なし


### n=8 k=6 — pass

取得経路: structured

TeX: `\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}^{2}\}`

検出事項: なし

- ν8^2: Element=[4, 4], source=14, target=8, issues=[]

### n=8 k=7 — pass

取得経路: structured

TeX: `\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}`

検出事項: なし

- σ8: Element=[9], source=15, target=8, issues=[]
- E σ': Element=[8], source=15, target=8, issues=[]

### n=9 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{9}^{9} = \mathbb{Z}\{\iota_{9}\}`

検出事項: なし

- ι9: Element=[1], source=9, target=9, issues=[]

### n=9 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{10}^{9} = \mathbb{Z}/2\{\eta_{9}\}`

検出事項: なし

- η9: Element=[2], source=10, target=9, issues=[]

### n=9 k=2 — pass

取得経路: structured

TeX: `\pi_{11}^{9} = \mathbb{Z}/2\{\eta_{9}^{2}\}`

検出事項: なし

- η9^2: Element=[2, 2], source=11, target=9, issues=[]

### n=9 k=3 — pass

取得経路: structured

TeX: `\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}`

検出事項: なし

- ν9: Element=[4], source=12, target=9, issues=[]

### n=9 k=4 — pass

取得経路: zero

TeX: `\pi_{13}^{9} = 0`

検出事項: なし


### n=9 k=5 — pass

取得経路: zero

TeX: `\pi_{14}^{9} = 0`

検出事項: なし


### n=9 k=6 — pass

取得経路: structured

TeX: `\pi_{15}^{9} = \mathbb{Z}/2\{\nu_{9}^{2}\}`

検出事項: なし

- ν9^2: Element=[4, 4], source=15, target=9, issues=[]

### n=9 k=7 — pass

取得経路: structured

TeX: `\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}`

検出事項: なし

- σ9: Element=[9], source=16, target=9, issues=[]

### n=10 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{10}^{10} = \mathbb{Z}\{\iota_{10}\}`

検出事項: なし

- ι2: Element=[1], source=10, target=10, issues=[]

### n=10 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{11}^{10} = \mathbb{Z}/2\{\eta_{10}\}`

検出事項: なし

- η3: Element=[2], source=11, target=10, issues=[]

### n=10 k=2 — pass

取得経路: structured

TeX: `\pi_{12}^{10} = \mathbb{Z}/2\{\eta_{10}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=12, target=10, issues=[]

### n=10 k=3 — pass

取得経路: structured

TeX: `\pi_{13}^{10} = \mathbb{Z}/8\{\nu_{10}\}`

検出事項: なし

- ν5: Element=[4], source=13, target=10, issues=[]

### n=10 k=4 — pass

取得経路: zero

TeX: `\pi_{14}^{10} = 0`

検出事項: なし


### n=10 k=5 — pass

取得経路: zero

TeX: `\pi_{15}^{10} = 0`

検出事項: なし


### n=10 k=6 — pass

取得経路: structured

TeX: `\pi_{16}^{10} = \mathbb{Z}/2\{\nu_{10}^{2}\}`

検出事項: なし

- ν8^2: Element=[4, 4], source=16, target=10, issues=[]

### n=10 k=7 — pass

取得経路: structured

TeX: `\pi_{17}^{10} = \mathbb{Z}/16\{\sigma_{10}\}`

検出事項: なし

- σ10: Element=[9], source=17, target=10, issues=[]

### n=11 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{11}^{11} = \mathbb{Z}\{\iota_{11}\}`

検出事項: なし

- ι11: Element=[1], source=11, target=11, issues=[]

### n=11 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{12}^{11} = \mathbb{Z}/2\{\eta_{11}\}`

検出事項: なし

- η11: Element=[2], source=12, target=11, issues=[]

### n=11 k=2 — pass

取得経路: structured

TeX: `\pi_{13}^{11} = \mathbb{Z}/2\{\eta_{11}^{2}\}`

検出事項: なし

- η11^2: Element=[2, 2], source=13, target=11, issues=[]

### n=11 k=3 — pass

取得経路: structured

TeX: `\pi_{14}^{11} = \mathbb{Z}/8\{\nu_{11}\}`

検出事項: なし

- ν11: Element=[4], source=14, target=11, issues=[]

### n=11 k=4 — pass

取得経路: zero

TeX: `\pi_{15}^{11} = 0`

検出事項: なし


### n=11 k=5 — pass

取得経路: zero

TeX: `\pi_{16}^{11} = 0`

検出事項: なし


### n=11 k=6 — pass

取得経路: structured

TeX: `\pi_{17}^{11} = \mathbb{Z}/2\{\nu_{11}^{2}\}`

検出事項: なし

- ν11^2: Element=[4, 4], source=17, target=11, issues=[]

### n=11 k=7 — pass

取得経路: structured

TeX: `\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}`

検出事項: なし

- σ11: Element=[9], source=18, target=11, issues=[]

### n=12 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{12}^{12} = \mathbb{Z}\{\iota_{12}\}`

検出事項: なし

- ι2: Element=[1], source=12, target=12, issues=[]

### n=12 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{13}^{12} = \mathbb{Z}/2\{\eta_{12}\}`

検出事項: なし

- η3: Element=[2], source=13, target=12, issues=[]

### n=12 k=2 — pass

取得経路: structured

TeX: `\pi_{14}^{12} = \mathbb{Z}/2\{\eta_{12}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=14, target=12, issues=[]

### n=12 k=3 — pass

取得経路: structured

TeX: `\pi_{15}^{12} = \mathbb{Z}/8\{\nu_{12}\}`

検出事項: なし

- ν5: Element=[4], source=15, target=12, issues=[]

### n=12 k=4 — pass

取得経路: zero

TeX: `\pi_{16}^{12} = 0`

検出事項: なし


### n=12 k=5 — pass

取得経路: zero

TeX: `\pi_{17}^{12} = 0`

検出事項: なし


### n=12 k=6 — pass

取得経路: structured

TeX: `\pi_{18}^{12} = \mathbb{Z}/2\{\nu_{12}^{2}\}`

検出事項: なし

- ν8^2: Element=[4, 4], source=18, target=12, issues=[]

### n=12 k=7 — pass

取得経路: structured

TeX: `\pi_{19}^{12} = \mathbb{Z}/16\{\sigma_{12}\}`

検出事項: なし

- σ9: Element=[9], source=19, target=12, issues=[]

### n=13 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{13}^{13} = \mathbb{Z}\{\iota_{13}\}`

検出事項: なし

- ι13: Element=[1], source=13, target=13, issues=[]

### n=13 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{14}^{13} = \mathbb{Z}/2\{\eta_{13}\}`

検出事項: なし

- η13: Element=[2], source=14, target=13, issues=[]

### n=13 k=2 — pass

取得経路: structured

TeX: `\pi_{15}^{13} = \mathbb{Z}/2\{\eta_{13}^{2}\}`

検出事項: なし

- η13^2: Element=[2, 2], source=15, target=13, issues=[]

### n=13 k=3 — pass

取得経路: structured

TeX: `\pi_{16}^{13} = \mathbb{Z}/8\{\nu_{13}\}`

検出事項: なし

- ν13: Element=[4], source=16, target=13, issues=[]

### n=13 k=4 — pass

取得経路: zero

TeX: `\pi_{17}^{13} = 0`

検出事項: なし


### n=13 k=5 — pass

取得経路: zero

TeX: `\pi_{18}^{13} = 0`

検出事項: なし


### n=13 k=6 — pass

取得経路: structured

TeX: `\pi_{19}^{13} = \mathbb{Z}/2\{\nu_{13}^{2}\}`

検出事項: なし

- ν13^2: Element=[4, 4], source=19, target=13, issues=[]

### n=13 k=7 — pass

取得経路: structured

TeX: `\pi_{20}^{13} = \mathbb{Z}/16\{\sigma_{13}\}`

検出事項: なし

- σ13: Element=[9], source=20, target=13, issues=[]

### n=14 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{14}^{14} = \mathbb{Z}\{\iota_{14}\}`

検出事項: なし

- ι2: Element=[1], source=14, target=14, issues=[]

### n=14 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{15}^{14} = \mathbb{Z}/2\{\eta_{14}\}`

検出事項: なし

- η3: Element=[2], source=15, target=14, issues=[]

### n=14 k=2 — pass

取得経路: structured

TeX: `\pi_{16}^{14} = \mathbb{Z}/2\{\eta_{14}^{2}\}`

検出事項: なし

- η4^2: Element=[2, 2], source=16, target=14, issues=[]

### n=14 k=3 — pass

取得経路: structured

TeX: `\pi_{17}^{14} = \mathbb{Z}/8\{\nu_{14}\}`

検出事項: なし

- ν5: Element=[4], source=17, target=14, issues=[]

### n=14 k=4 — pass

取得経路: zero

TeX: `\pi_{18}^{14} = 0`

検出事項: なし


### n=14 k=5 — pass

取得経路: zero

TeX: `\pi_{19}^{14} = 0`

検出事項: なし


### n=14 k=6 — pass

取得経路: structured

TeX: `\pi_{20}^{14} = \mathbb{Z}/2\{\nu_{14}^{2}\}`

検出事項: なし

- ν8^2: Element=[4, 4], source=20, target=14, issues=[]

### n=14 k=7 — pass

取得経路: structured

TeX: `\pi_{21}^{14} = \mathbb{Z}/16\{\sigma_{14}\}`

検出事項: なし

- σ9: Element=[9], source=21, target=14, issues=[]

### n=15 k=0 — partially_verified

取得経路: simple

TeX: `\pi_{15}^{15} = \mathbb{Z}\{\iota_{15}\}`

検出事項: なし

- ι15: Element=[1], source=15, target=15, issues=[]

### n=15 k=1 — partially_verified

取得経路: simple

TeX: `\pi_{16}^{15} = \mathbb{Z}/2\{\eta_{15}\}`

検出事項: なし

- η15: Element=[2], source=16, target=15, issues=[]

### n=15 k=2 — pass

取得経路: structured

TeX: `\pi_{17}^{15} = \mathbb{Z}/2\{\eta_{15}^{2}\}`

検出事項: なし

- η15^2: Element=[2, 2], source=17, target=15, issues=[]

### n=15 k=3 — pass

取得経路: structured

TeX: `\pi_{18}^{15} = \mathbb{Z}/8\{\nu_{15}\}`

検出事項: なし

- ν15: Element=[4], source=18, target=15, issues=[]

### n=15 k=4 — pass

取得経路: zero

TeX: `\pi_{19}^{15} = 0`

検出事項: なし


### n=15 k=5 — pass

取得経路: zero

TeX: `\pi_{20}^{15} = 0`

検出事項: なし


### n=15 k=6 — pass

取得経路: structured

TeX: `\pi_{21}^{15} = \mathbb{Z}/2\{\nu_{15}^{2}\}`

検出事項: なし

- ν15^2: Element=[4, 4], source=21, target=15, issues=[]

### n=15 k=7 — pass

取得経路: structured

TeX: `\pi_{22}^{15} = \mathbb{Z}/16\{\sigma_{15}\}`

検出事項: なし

- σ15: Element=[9], source=22, target=15, issues=[]
