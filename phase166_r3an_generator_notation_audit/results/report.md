# Phase 166 R3-AN 生成元表記監査

## 集計

```json
{
  "phase": "166-r3an-generator-notation-audit",
  "count": 112,
  "source_counts": {
    "simple": 28,
    "structured": 61,
    "zero": 23
  },
  "issue_counts": {},
  "pass": 112,
  "production_code_modified": false,
  "proof_search_executed": false,
  "scope": "structural consistency and LaTeX output; not full mathematical equivalence or browser rendering"
}
```

## 個別表示

### n=2, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{2}^{2} = \mathbb{Z}\{\iota_{2}\}
```

### n=2, k=1 — simple / OK

DB: `['η2']`

```tex
\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}
```

### n=2, k=2 — structured / OK

DB: `['η2^2']`

```tex
\pi_{4}^{2} = \mathbb{Z}/2\{\eta_{2}^{2}\}
```

### n=2, k=3 — structured / OK

DB: `['η2^3']`

```tex
\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}
```

### n=2, k=4 — structured / OK

DB: `["η2ν'"]`

```tex
\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}
```

### n=2, k=5 — structured / OK

DB: `["η2ν'η6"]`

```tex
\pi_{7}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\}
```

### n=2, k=6 — structured / OK

DB: `["η2ν'η6^2"]`

```tex
\pi_{8}^{2} = \mathbb{Z}/2\{\eta_{2}\nu'\eta_{6}\eta_{7}\}
```

### n=2, k=7 — zero / OK

DB: `['0']`

```tex
\pi_{9}^{2} = 0
```

### n=3, k=0 — simple / OK

DB: `['ι3']`

```tex
\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}
```

### n=3, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}
```

### n=3, k=2 — structured / OK

DB: `['η3^2']`

```tex
\pi_{5}^{3} = \mathbb{Z}/2\{\eta_{3}^{2}\}
```

### n=3, k=3 — structured / OK

DB: `["ν'"]`

```tex
\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}
```

### n=3, k=4 — structured / OK

DB: `["ν'η6"]`

```tex
\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}
```

### n=3, k=5 — structured / OK

DB: `["ν'η6^2"]`

```tex
\pi_{8}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\eta_{7}\}
```

### n=3, k=6 — zero / OK

DB: `['0']`

```tex
\pi_{9}^{3} = 0
```

### n=3, k=7 — zero / OK

DB: `['0']`

```tex
\pi_{10}^{3} = 0
```

### n=4, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{4}^{4} = \mathbb{Z}\{\iota_{4}\}
```

### n=4, k=1 — simple / OK

DB: `['η4']`

```tex
\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}
```

### n=4, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{6}^{4} = \mathbb{Z}/2\{\eta_{4}^{2}\}
```

### n=4, k=3 — structured / OK

DB: `['ν4', "E ν'"]`

```tex
\pi_{7}^{4} = \mathbb{Z}\{\nu_{4}\} \oplus \mathbb{Z}/4\{E\nu'\}
```

### n=4, k=4 — structured / OK

DB: `['ν4η7', "E ν'η7"]`

```tex
\pi_{8}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\}
```

### n=4, k=5 — structured / OK

DB: `['ν4η7^2', "E ν'η7^2"]`

```tex
\pi_{9}^{4} = \mathbb{Z}/2\{\nu_{4}\eta_{7}\eta_{8}\} \oplus \mathbb{Z}/2\{E\nu'\eta_{7}\eta_{8}\}
```

### n=4, k=6 — structured / OK

DB: `['ν4^2']`

```tex
\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}^{2}\}
```

### n=4, k=7 — zero / OK

DB: `['0']`

```tex
\pi_{11}^{4} = 0
```

### n=5, k=0 — simple / OK

DB: `['ι5']`

```tex
\pi_{5}^{5} = \mathbb{Z}\{\iota_{5}\}
```

### n=5, k=1 — simple / OK

DB: `['η5']`

```tex
\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}
```

### n=5, k=2 — structured / OK

DB: `['η5^2']`

```tex
\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}
```

### n=5, k=3 — structured / OK

DB: `['ν5']`

```tex
\pi_{8}^{5} = \mathbb{Z}/8\{\nu_{5}\}
```

### n=5, k=4 — structured / OK

DB: `['ν5η8']`

```tex
\pi_{9}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\}
```

### n=5, k=5 — structured / OK

DB: `['ν5η8^2']`

```tex
\pi_{10}^{5} = \mathbb{Z}/2\{\nu_{5}\eta_{8}\eta_{9}\}
```

### n=5, k=6 — structured / OK

DB: `['ν5^2']`

```tex
\pi_{11}^{5} = \mathbb{Z}/2\{\nu_{5}^{2}\}
```

### n=5, k=7 — structured / OK

DB: `["σ'''"]`

```tex
\pi_{12}^{5} = \mathbb{Z}/2\{\sigma'''\}
```

### n=6, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{6}^{6} = \mathbb{Z}\{\iota_{6}\}
```

### n=6, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{7}^{6} = \mathbb{Z}/2\{\eta_{6}\}
```

### n=6, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{8}^{6} = \mathbb{Z}/2\{\eta_{6}^{2}\}
```

### n=6, k=3 — structured / OK

DB: `['ν6']`

```tex
\pi_{9}^{6} = \mathbb{Z}/8\{\nu_{6}\}
```

### n=6, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{10}^{6} = 0
```

### n=6, k=5 — structured / OK

DB: `['\\Delta(ι13)']`

```tex
\pi_{11}^{6} = \mathbb{Z}\{\Delta(\iota13)\}
```

### n=6, k=6 — structured / OK

DB: `['ν6^2']`

```tex
\pi_{12}^{6} = \mathbb{Z}/2\{\nu_{6}^{2}\}
```

### n=6, k=7 — structured / OK

DB: `["σ''"]`

```tex
\pi_{13}^{6} = \mathbb{Z}/4\{\sigma''\}
```

### n=7, k=0 — simple / OK

DB: `['ι7']`

```tex
\pi_{7}^{7} = \mathbb{Z}\{\iota_{7}\}
```

### n=7, k=1 — simple / OK

DB: `['η7']`

```tex
\pi_{8}^{7} = \mathbb{Z}/2\{\eta_{7}\}
```

### n=7, k=2 — structured / OK

DB: `['η7^2']`

```tex
\pi_{9}^{7} = \mathbb{Z}/2\{\eta_{7}^{2}\}
```

### n=7, k=3 — structured / OK

DB: `['ν7']`

```tex
\pi_{10}^{7} = \mathbb{Z}/8\{\nu_{7}\}
```

### n=7, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{11}^{7} = 0
```

### n=7, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{12}^{7} = 0
```

### n=7, k=6 — structured / OK

DB: `['ν7^2']`

```tex
\pi_{13}^{7} = \mathbb{Z}/2\{\nu_{7}^{2}\}
```

### n=7, k=7 — structured / OK

DB: `["σ'"]`

```tex
\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}
```

### n=8, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{8}^{8} = \mathbb{Z}\{\iota_{8}\}
```

### n=8, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{9}^{8} = \mathbb{Z}/2\{\eta_{8}\}
```

### n=8, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{10}^{8} = \mathbb{Z}/2\{\eta_{8}^{2}\}
```

### n=8, k=3 — structured / OK

DB: `['ν5']`

```tex
\pi_{11}^{8} = \mathbb{Z}/8\{\nu_{8}\}
```

### n=8, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{12}^{8} = 0
```

### n=8, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{13}^{8} = 0
```

### n=8, k=6 — structured / OK

DB: `['ν8^2']`

```tex
\pi_{14}^{8} = \mathbb{Z}/2\{\nu_{8}^{2}\}
```

### n=8, k=7 — structured / OK

DB: `['σ8', "E σ'"]`

```tex
\pi_{15}^{8} = \mathbb{Z}\{\sigma_{8}\} \oplus \mathbb{Z}/8\{E\sigma'\}
```

### n=9, k=0 — simple / OK

DB: `['ι9']`

```tex
\pi_{9}^{9} = \mathbb{Z}\{\iota_{9}\}
```

### n=9, k=1 — simple / OK

DB: `['η9']`

```tex
\pi_{10}^{9} = \mathbb{Z}/2\{\eta_{9}\}
```

### n=9, k=2 — structured / OK

DB: `['η9^2']`

```tex
\pi_{11}^{9} = \mathbb{Z}/2\{\eta_{9}^{2}\}
```

### n=9, k=3 — structured / OK

DB: `['ν9']`

```tex
\pi_{12}^{9} = \mathbb{Z}/8\{\nu_{9}\}
```

### n=9, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{13}^{9} = 0
```

### n=9, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{14}^{9} = 0
```

### n=9, k=6 — structured / OK

DB: `['ν9^2']`

```tex
\pi_{15}^{9} = \mathbb{Z}/2\{\nu_{9}^{2}\}
```

### n=9, k=7 — structured / OK

DB: `['σ9']`

```tex
\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}
```

### n=10, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{10}^{10} = \mathbb{Z}\{\iota_{10}\}
```

### n=10, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{11}^{10} = \mathbb{Z}/2\{\eta_{10}\}
```

### n=10, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{12}^{10} = \mathbb{Z}/2\{\eta_{10}^{2}\}
```

### n=10, k=3 — structured / OK

DB: `['ν5']`

```tex
\pi_{13}^{10} = \mathbb{Z}/8\{\nu_{10}\}
```

### n=10, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{14}^{10} = 0
```

### n=10, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{15}^{10} = 0
```

### n=10, k=6 — structured / OK

DB: `['ν8^2']`

```tex
\pi_{16}^{10} = \mathbb{Z}/2\{\nu_{10}^{2}\}
```

### n=10, k=7 — structured / OK

DB: `['σ10']`

```tex
\pi_{17}^{10} = \mathbb{Z}/16\{\sigma_{10}\}
```

### n=11, k=0 — simple / OK

DB: `['ι11']`

```tex
\pi_{11}^{11} = \mathbb{Z}\{\iota_{11}\}
```

### n=11, k=1 — simple / OK

DB: `['η11']`

```tex
\pi_{12}^{11} = \mathbb{Z}/2\{\eta_{11}\}
```

### n=11, k=2 — structured / OK

DB: `['η11^2']`

```tex
\pi_{13}^{11} = \mathbb{Z}/2\{\eta_{11}^{2}\}
```

### n=11, k=3 — structured / OK

DB: `['ν11']`

```tex
\pi_{14}^{11} = \mathbb{Z}/8\{\nu_{11}\}
```

### n=11, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{15}^{11} = 0
```

### n=11, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{16}^{11} = 0
```

### n=11, k=6 — structured / OK

DB: `['ν11^2']`

```tex
\pi_{17}^{11} = \mathbb{Z}/2\{\nu_{11}^{2}\}
```

### n=11, k=7 — structured / OK

DB: `['σ11']`

```tex
\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}
```

### n=12, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{12}^{12} = \mathbb{Z}\{\iota_{12}\}
```

### n=12, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{13}^{12} = \mathbb{Z}/2\{\eta_{12}\}
```

### n=12, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{14}^{12} = \mathbb{Z}/2\{\eta_{12}^{2}\}
```

### n=12, k=3 — structured / OK

DB: `['ν5']`

```tex
\pi_{15}^{12} = \mathbb{Z}/8\{\nu_{12}\}
```

### n=12, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{16}^{12} = 0
```

### n=12, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{17}^{12} = 0
```

### n=12, k=6 — structured / OK

DB: `['ν8^2']`

```tex
\pi_{18}^{12} = \mathbb{Z}/2\{\nu_{12}^{2}\}
```

### n=12, k=7 — structured / OK

DB: `['σ9']`

```tex
\pi_{19}^{12} = \mathbb{Z}/16\{\sigma_{12}\}
```

### n=13, k=0 — simple / OK

DB: `['ι13']`

```tex
\pi_{13}^{13} = \mathbb{Z}\{\iota_{13}\}
```

### n=13, k=1 — simple / OK

DB: `['η13']`

```tex
\pi_{14}^{13} = \mathbb{Z}/2\{\eta_{13}\}
```

### n=13, k=2 — structured / OK

DB: `['η13^2']`

```tex
\pi_{15}^{13} = \mathbb{Z}/2\{\eta_{13}^{2}\}
```

### n=13, k=3 — structured / OK

DB: `['ν13']`

```tex
\pi_{16}^{13} = \mathbb{Z}/8\{\nu_{13}\}
```

### n=13, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{17}^{13} = 0
```

### n=13, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{18}^{13} = 0
```

### n=13, k=6 — structured / OK

DB: `['ν13^2']`

```tex
\pi_{19}^{13} = \mathbb{Z}/2\{\nu_{13}^{2}\}
```

### n=13, k=7 — structured / OK

DB: `['σ13']`

```tex
\pi_{20}^{13} = \mathbb{Z}/16\{\sigma_{13}\}
```

### n=14, k=0 — simple / OK

DB: `['ι2']`

```tex
\pi_{14}^{14} = \mathbb{Z}\{\iota_{14}\}
```

### n=14, k=1 — simple / OK

DB: `['η3']`

```tex
\pi_{15}^{14} = \mathbb{Z}/2\{\eta_{14}\}
```

### n=14, k=2 — structured / OK

DB: `['η4^2']`

```tex
\pi_{16}^{14} = \mathbb{Z}/2\{\eta_{14}^{2}\}
```

### n=14, k=3 — structured / OK

DB: `['ν5']`

```tex
\pi_{17}^{14} = \mathbb{Z}/8\{\nu_{14}\}
```

### n=14, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{18}^{14} = 0
```

### n=14, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{19}^{14} = 0
```

### n=14, k=6 — structured / OK

DB: `['ν8^2']`

```tex
\pi_{20}^{14} = \mathbb{Z}/2\{\nu_{14}^{2}\}
```

### n=14, k=7 — structured / OK

DB: `['σ9']`

```tex
\pi_{21}^{14} = \mathbb{Z}/16\{\sigma_{14}\}
```

### n=15, k=0 — simple / OK

DB: `['ι15']`

```tex
\pi_{15}^{15} = \mathbb{Z}\{\iota_{15}\}
```

### n=15, k=1 — simple / OK

DB: `['η15']`

```tex
\pi_{16}^{15} = \mathbb{Z}/2\{\eta_{15}\}
```

### n=15, k=2 — structured / OK

DB: `['η15^2']`

```tex
\pi_{17}^{15} = \mathbb{Z}/2\{\eta_{15}^{2}\}
```

### n=15, k=3 — structured / OK

DB: `['ν15']`

```tex
\pi_{18}^{15} = \mathbb{Z}/8\{\nu_{15}\}
```

### n=15, k=4 — zero / OK

DB: `['0']`

```tex
\pi_{19}^{15} = 0
```

### n=15, k=5 — zero / OK

DB: `['0']`

```tex
\pi_{20}^{15} = 0
```

### n=15, k=6 — structured / OK

DB: `['ν15^2']`

```tex
\pi_{21}^{15} = \mathbb{Z}/2\{\nu_{15}^{2}\}
```

### n=15, k=7 — structured / OK

DB: `['σ15']`

```tex
\pi_{22}^{15} = \mathbb{Z}/16\{\sigma_{15}\}
```
