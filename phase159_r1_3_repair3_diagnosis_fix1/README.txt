Phase 159-R1-3 repair3 diagnosis fix1

前回の diagnosis failure は production code の問題ではない。

原因:
サブディレクトリ内の Python script を直接実行したため、
repository root が import path に入らず、
toda_calculation_facade を import できなかった。

fix1:
PowerShell runner で PYTHONPATH に repository root を追加する。

production code changes:
none

test changes:
none

この診断結果をそのままチャットへ貼る。
