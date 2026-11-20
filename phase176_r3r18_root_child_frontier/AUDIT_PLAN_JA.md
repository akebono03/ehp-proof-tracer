# Phase 176 R3R18 監査計画

## 目的

R3R17 の根候補3件について、各候補が要求する直接の子 Goal を列挙し、再帰探索の次の未解決境界を特定する。候補の存在を証明完了と混同しない。

## 変更対象

- 新規 `phase176_r3r18_root_child_frontier/audit.py`：`source_guard`、`summarize`、`observe`、`output_path`、`execute`、`main` を追加。
- 新規 `phase176_r3r18_root_child_frontier/tests/test_audit.py`：3件の限定テスト。
- 新規 `phase176_r3r18_root_child_frontier/run.ps1`。
- 新規 `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 監査条件

Git `develop`、追跡ファイル clean、既存実装のアンカー存在を確認。Group query `(3,5)` を読み取り専用で実行。根の候補・直接の子 Goal・子候補数・出典候補数を JSON に保存。

## 境界

- 既存コード・GIVEN・Provider の変更なし。
- 前段の二段階零像証明を新たな根の証明に昇格させない。
- 全体 pytest は実行しない。
- 子候補の存在だけで証明済みとしない。
