# Phase 174 R3-R7-R11：監査用合成式の型再確認

## 目的

R10 の実測結果は、元の ν 懸垂像が0候補、引用済みの正規 ν 懸垂像が1候補、始域の ν 生成元が正規形、終域だけが不一致であったことを示す。

R7〜R10 で監査用に手作成した `HomotopyElement("nu_6", ..., GeneratorSymbol("nu", 6))` は、実際の登録済み ν 系列が用いる `GeneratorSymbol("ν", 6)` と**等しくない**。同様の `eta` / `η` 差もある。

この事実だけから別名同一性を証明することはできない。新しい別名規則を導入せず、登録済み ν・η ファミリー ID・次元・始域終域に基づき、**別の監査候補**を組み立てて候補数を測定する。

## 対象ファイル・関数

新規 `phase174_r3_r7_r11_canonical_fixture_audit/` のみ。 `audit.py` に `git`, `reviewed_head_lineage`, `verify_git_and_sources`, `prior_report_path`, `validate_r10_evidence`, `strict_family_comparison`, `inspect_live_frontier`, `output_path`, `make_report`, `main` を新設。`tests/test_audit.py` に全テストを新設し、`run.ps1` で独立プロセスの限定 pytest を実行する。

既存のソース・クラス・関数・テスト・README.md・docs/design.md・development_log.md・roadmap.md・proof_records.md は変更しない。

## 監査の境界

- GitHub `develop` と SHA 固定した14ファイル、前工程の R10 JSON を検証する。
- ν-family ID=4 と η-family ID=2 から、登録された名前・記号・型で別の合成懸垂候補を作る。
- 正規候補・過去の監査用候補の `GeneratorImage`、`Relation` の公開候補数を比較する。
- 同じ名前でも `GeneratorSymbol` が異なれば同一視しない。
- Toda (5.9) の採用転写と検証済み ProofStep は同一視しない。
- 新規の GIVEN、production rule、公開経路、Narrative を作らない。数学的完成を宣言しない。

## テストと次段階

R11、R10〜R3、数学回帰、family 回帰だけを限定実行。全体 pytest は Phase 174 の終了時のみ。

R11 の結果で正規化した左因子の零関係まで本当に候補が無い場合に、次段階で Toda (5.9) の採用位置・独立推論を監査する。表示・推論の専用分岐を追加しない。
