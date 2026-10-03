Phase157 R11-R7 repair1

前回の R11-R7 patch は途中適用された。

適用済み:
- (5.3) Hopf component retain
- Reference/body exact duplicate -> [R#]より
- first connector 次に -> まず
- helper functions の追加

停止した箇所:
- renderer pipeline への helper 呼び出し追加

repair1 は現在の部分適用状態を前提にし、
適用済み変更を重複適用せず、残りだけを適用する。

repair1:
- pipeline call insertion
- public display-math period normalization
- FINAL_RESULT_DERIVATION filler suppression
- historical focused test opener expectation update
- R11-R7 focused regression tests

full repository pytest は Phase157 closure まで実行しない。
