# Phase 159-R1-7b repair13 matching runtime diagnosis

## Exactness candidates

### candidate 1

`'\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2}'`

### candidate 2

`'\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5}'`

## Baseline proof body

### line 0

- repr: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は全射である.'`
- startswith 完全性より,: False
- equals 完全性より,: False
- signature: ('\\Delta', '\\pi_{10}^{5}', '\\pi_{8}^{2}')
- matching candidates: ('\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2}',)

### line 4

- repr: `'$\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5}$.'`
- startswith 完全性より,: False
- equals 完全性より,: False
- signature: None
- matching candidates: ()

### line 6

- repr: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は単射である.'`
- startswith 完全性より,: False
- equals 完全性より,: False
- signature: ('\\Delta', '\\pi_{10}^{5}', '\\pi_{8}^{2}')
- matching candidates: ('\\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5} \\xrightarrow{\\Delta} \\pi_{8}^{2}',)

## Normalized relevant lines

- 0: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は全射である.'`
- 4: `'\\['`
- 5: `'\\pi_{9}^{2} \\xrightarrow{E} \\pi_{10}^{3} \\xrightarrow{H} \\pi_{10}^{5}.'`
- 6: `'\\]'`
- 9: `'$\\Delta: \\pi_{10}^{5} \\to \\pi_{8}^{2}$ は単射である.'`
