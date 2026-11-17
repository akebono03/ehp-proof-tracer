# Phase 175 R3R11R4 — テスト記録

## R3R11R3 実行失敗の記録

ユーザー Windows 実行：DryRun `PASS_R3R11R3_READ_ONLY_DRYRUN`、`PATCH_STATUS=ALREADY_APPLIED`。本実行の限定 pytest は `34 passed, 1 failed`。失敗は Phase 172 の `$\pi_6^3$` Hopf narrative regression、`test_real_public_narrative_shortens_hopf_chain_only`。

## R3R11R4 作成環境で実施

- `python -m compileall`：構文確認 PASS。
- `python -m pytest -q -p no:cacheprovider -o addopts= phase175_r3r11_cited_hopf_narrative/tests/test_install.py`：**6 passed**。
- ZIP 構成およびソースハッシュ：生成後の ZIP 整合性チェックを行う。
- 新しい `test_projection.py` の実行：本作成環境には完全なアプリケーションリポジトリがないため **未実施**。Windows 本実行に委ねる。

## Windows に委ねる限定テスト

`audit.py` の `TEST_PATHS`。従来の Phase 172 テストと新規 $\pi_6^3$ 回帰テストを両方含む。全体 pytest は行わない。

## 完了条件

- DryRun `PASS_R3R11R4_READ_ONLY_DRYRUN`、終了コード0。
- 本実行の限定 pytest 全件 PASS。
- $\pi_6^3$ の Phase 172 表示維持。
- $\pi_7^3$ の1本の Hopf 連鎖を維持。
- 公開証明：complete、Web generic-complete-proof、Trust True、Reference 7件、Lemma 5.4 非依存。
- 最終 `PASS_R3R11R4_SINGLE_EQUATION_AND_PRIOR_NARRATIVE`。
