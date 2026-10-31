# Phase 171 R20R7R1 — コミット済み R20R6 基準への対応

## 原因と修正

R20R7 の初回配布は R20R6 が Git ワークツリー内で **未コミット**であることを前提としていた。ところが R20R6 が `develop` にコミットされたため、`git rev-parse HEAD:<path>` の Git blob ID が更新された。初回 DryRun はインストーラのガードで停止したので、今回の R20R7 は本番ファイルへ未適用。

GitHub の `develop` で実際の R20R6 コミット済みファイルを確認した。

| 対象 | R20R6 前の blob | R20R6 コミット後の blob |
|---|---|---|
| `phase171_r2j_r4_r7_nonzero_nu_order/source.py` | `5b95010681f6257dc46a4236c099445281635e53` | `340b66a90118a0760cd94eadaf192ad69f3c48b7` |
| `phase165_r52_r9_shared_math.py` | `10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac` | `c3a25c075f1dfa4573ce3feb1c07f653b0aa649a` |

`checked_worktree()` が完全にレビュー済みの2つの組み合わせを区別する。古い2 blob 組み合わせの場合は過去の R20R6 の差分を正確に再構成する。新しい2 blob 組み合わせでは `HEAD` 自体を R20R6 完成基準として採用する。古い・新しい blob の混在、未知の blob、予定外のワークツリー差分、R20R7 の片側のみ適用済みの状態は拒否する。HEAD の文字列そのものは固定しない。

## 実装・検証

- R20R7 の数学的推論、Citation（引用資格）、Web および既存 API に変更なし。
- 追加したガードテスト4件を含むインストーラ限定 pytest：7 PASS（この ZIP 作成環境）。
- 模擬 Git リポジトリに R20R6 をコミットした後の DryRun、本適用、再 DryRun、再本実行：PASS。バックアップ1セットと2つの予定ファイルのみの変更を確認。
- ユーザーの実リポジトリにおける R20R7 の限定 pytest、公開推論監査は未実施。
- 全体 pytest：Phase 171 完了時のみ。

## 完了条件と次工程の境界

R20R7 は `PHASE171_R20R7_INJECTED_ETA_IMAGE_NONZERO=CERTIFIED_PUBLIC_PROPOSAL_PRESENT`、限定 pytest PASS、新規 GIVEN 0件で完了とする。

R20R7 は $E(\eta_2^3)\neq 0$ への推論接続まで。$2\nu'\neq0$ と二倍等式の公開接続、$\pi_6^3$ の公開 `complete` 判定は次工程以降に残す。
