# Phase 165 R52-R11 — 共通 Renderer 統合

変更対象:
- `toda_group_proof_generic_narrative_renderer.py`
  - 新規関数 `render_toda_partial_proof_narrative_markdown` をファイル末尾に追加
- `phase165_r52_partial_proof.py`
  - 既存関数 `render_partial_proof_markdown` を全文置換し、共通 Renderer に委譲
- `test_phase165_r52_r11_common_renderer.py`
  - 5件の対象テストを追加

import: 既存のトップレベル import は変更なし。新規関数は内部 import を使用。
クラスの変更: なし。
証明探索・型付き命題・ルールの変更: なし。

重要:
既存の完成証明用 Presentation は単一の証明済み root を必要とする。
未完成証明は proof forest なので同じ Presentation 型には安全に格納できない。
そこで、既存の共通 generic narrative step renderer
`_render_generic_narrative_step` を使用する、同じ Renderer モジュールの
部分証明用入口に統合した。別の独立した数式 Renderer を作っていない。
`Goal` を偽の `ProofStep` に変換しない。未解決 Goal は独立して表示。
未解決 Goal の型が数式表示に未対応ならその型名を表示する。
Reference は PartialProofResult.references にあるものだけ表示。

インストール後に次の置換可能な全関数コードが出力される:
- INSTALLED_COMMON_FUNCTION_FULL.txt
- INSTALLED_WRAPPER_FULL.txt

実行:
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r52_r11_common_renderer.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r11_common_renderer\run.ps1"

対象 pytest だけ実行し、全体 pytest は Phase 末尾まで実施しない。
完了条件: R11/R10/R52 と R9/R8 の対象テストが成功すること。
次 Phase の境界: ProofStep 自体が0件の数学的探索改善は含まない。
