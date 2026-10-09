from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
MARK = '<!-- PHASE162_CLOSURE_20261010 -->'
SECTIONS = {
'README.md': r'''## Phase 162 — Proof Reconstruction and Reference Boundary Audit (2026-10-10)

Phase 162 continued the narrow unstable target $\pi_5^3$ and the suspension isomorphism $E:\pi_4^2\to\pi_5^3$. The work included goal-directed group-structure selection, existing-rule proof reconstruction, recursive `ProofStep` checks, and inspection of the connection to common Narrative output. These are bounded, concrete capabilities; the system does **not** yet provide general independent backward theorem search or guaranteed correct selection of all literature premises.

The audit exposed an architectural limitation: the existing literature references, structured statements, proof repositories, and statement-boundary components are distributed among several modules. In particular, there is no verified unified enforcement of the literary order of theorems, the order of claims inside one theorem, or the point at which each claim becomes available as a proved premise. A `locator` or presentation `order` alone does not establish proof eligibility. A referenced fixed statement should be treated as an external premise rather than automatically expanding its internal proof, and self-reference or later-theorem leakage must be prohibited.

**Phase 162 is closed for planning/documentation purposes with unresolved proof-search and reference-order issues.** This is not a claim that the $\pi_5^3$ proof, the public prose, or the general backward engine is complete. No pytest tests were run as part of this documentation update; repository-wide success is not claimed.

### Phase 163 — Unified Statement Registry (planned)

Phase 163 will inventory **all existing registered statements** (not just the $\pi_5^3$ dependencies), define stable statement/component identities, connect provenance and mathematical content, record source-order and proof-availability boundaries without guessing missing information, and offer a unified read/search interface. Existing mathematics, inference rules, `ProofStep` APIs, and renderer behavior should be preserved wherever possible. Unverified source positions must remain explicitly unknown rather than being assigned synthetic literary order.

### Later phase — General backward-search integration (planned)

Only after the registry and eligibility rules are audited should general backward rule discovery and source-constrained premise selection be connected to proof reconstruction. A complete registry is not equivalent to a complete theorem prover.
''',
'docs/design.md': r'''## Phase 162 終了時点の設計境界と Phase 163 方針（2026-10-10）

Phase 162 の $\pi_5^3$ 監査では、既存の `ProofStep` を利用した証明再構築と、結論から任意の出典を独立に発見する一般探索とを区別する必要が明確になった。既存の `phase161_r5_backward_proof_reconstruction.py` と `phase162_pi5_3_backward_selection.py` は限定された目標と既存の証拠に依存する。Reference と Proof 本文の表示だけを調整しても証明木の根拠選択の正しさは保証されない。

### 登録情報の責務分担

- `proof.py`: `LiteratureReference`、`ProofStep`、`InferenceRule` などの基礎型。
- `toda_rules.py` 等: 数学的 Statement と Production Rule。
- `theorem_facts.py` 等: 文献由来の事実。
- `proof_repository.py` / `standard_repository.py`: 証明ステップの登録・検索。
- `toda_literature_statement_boundary.py`: fixed statement と proof-internal fact の区別、および一部 component `order`。

これらは単一の検索・利用可能性判定契約ではない。特に component の `order` を、そのまま「先に証明済み」の証拠と解釈してはならない。

### Phase 163 の統一 Registry に必要な情報

文献識別子、命題識別子、主張識別子、構造化 Statement、適用範囲、出典 locator、文献内の掲載位置、同一命題内の主張順、主張が利用可能になる証明完了位置、proof-internal / fixed-statement 区分、依存関係、既存 `ProofStep` と `InferenceRule` の対応を共通に扱う。掲載位置と証明完了位置は異なる情報として保持する。複数の主張を同時に証明する場合は単純な直列番号で先行主張を利用可能にせず、依存グラフと同時証明の境界を扱う。

資料の順序や証明完了位置が不明なら `unknown` として扱い、推測した番号で証明探索を許可しない。異なる文献の間には自動的な全順序を置かない。自己参照、未証明の後続命題の引用、循環依存、同一命題の未確立主張の流用は探索の候補選択で拒否する設計とする。既に証明済みの fixed statement を引用する場合、その内部の Lemma や proof steps を引用のたびに自動展開しない。

### Phase 境界

Phase 162 は問題の特定と監査記録で区切る。Phase 163 は全登録 Statement の棚卸し・共通 ID・来歴・順序と利用資格のデータ整備および共通検索までとし、一般証明探索の成功を主張しない。一般 Backward Search の規則選択・候補評価への統合は後続 Phase とする。既存 API と数学的推論規則の変更は必要最小限とする。
''',
'docs/roadmap.md': r'''## Phase 162 — 終了時点の判断（2026-10-10）

$\pi_5^3$ の Backward Reconstruction（逆向き証明再構築）と Narrative 接続の監査を進めた。`ProofStep` の再利用、文献出典の帰属、不要な内部証明の混入、Reference と Proof 本文の境界、推論の順序を確認したが、任意目標からの一般的な文献選択や、掲載順による引用資格判定は未完成である。Phase 162 は**監査・計画上の区切り**とし、数学的な一般自動証明の完成や全体テスト成功は主張しない。

## Phase 163 — 全登録命題の統一管理（次 Phase）

1. Production に登録された全 Statement / Reference / `ProofStep` / `InferenceRule` を横断的に棚卸しし、重複・未対応・出典不明を可視化する。
2. 文献・命題・命題内主張の安定識別子を定義する。数学的 Statement の型と適用範囲は再利用する。
3. 命題掲載順、命題内の主張順、証明完了による利用可能位置、依存関係を別々に記録する。不明情報は未確認のまま保持する。
4. fixed statement と proof-internal fact を区別し、外部引用の際に証明内部を無条件に展開しない。
5. 既存 API を壊さず統一 Registry から全登録 Statement を検索・照合可能にする。循環・自己引用・未確立の後続主張の使用を検出する軽量な局所テストを段階的に整備する。

**完了条件**: 既存の全登録対象について統一検索のカバレッジを監査でき、出典・主張順・利用可能性を判定できるか、不明として明示できること。未確認の掲載順から許可を捏造しない。

## Phase 164（仮）— Backward Search への統合

Phase 163 で統一した登録情報を、一般的な推論規則選択と根拠探索に接続する。まず $\pi_5^3$ を代表例として、既存の完成証明木や後続命題への依存がないことを確認し、その後に他の非安定群へ広げる。Phase 163 ではこの機能を先取りしない。

## 今回の検証境界

2026-10-10 の文書更新では pytest を実行しない。全体テストは実装 Phase の終わりにのみ実行する方針とし、今回の Phase 162 文書区切りをテスト完了と混同しない。
''',
'docs/development_log.md': r'''## Phase 162 — 証明木と Reference の責務監査、文書上の区切り（2026-10-10）

Phase 161 で導入した具体的 Backward Goal Reconstruction を受け、Phase 162 では $\pi_5^3$ の群構造、$E:\pi_4^2\to\pi_5^3$ の同型性、既存 `ProofStep` に基づく証明構築と共通 Narrative 接続を確認した。途中で生成された文章と、結論から独立に組み立てた証明木の区別が必要と判明した。`(5.3)` を fixed Reference として利用する場合、Lemma 5.2 などその証明内部の根拠を同時に本文へ自動展開すべきでないという問題、Reference 内の命題と proof-internal fact の混在、不要枝や説明の混入が監査課題として残った。

2026-10-10 の設計議論により、現行の登録情報が `toda_rules.py`、`theorem_facts.py`、`proof_repository.py`、`standard_repository.py`、`toda_literature_statement_boundary.py` 等に分散し、命題ごとの掲載順と同一命題内の主張順・証明完了順を統一的に用いて候補を制限できる保証がないと整理した。`toda_literature_statement_boundary.py` の一部 component には `order` があるが、それは直ちに利用可能性の根拠にはならない。

Phase 162 は未解決事項を次 Phase に引き継ぐ**文書上の区切り**とし、一般的な Backward Search、証明全体の妥当性、Narrative の完成を達成済みとは扱わない。次 Phase 163 は登録済みの**全**命題・主張を対象とする統一 Statement Registry の整備と引用順序のモデル化。一般的な規則選択・証明探索への適用は後続 Phase に分離する。

今回のドキュメント更新では**pytest は一切実行していない**。全体テストの PASS は主張しない。既存の過去記録は保持した。
''',
'docs/proof_records.md': r'''## Phase 162 — $\pi_5^3$ 証明木の未解決境界（2026-10-10）

対象目標：

$$
\pi_5^3=\mathbb Z/2\{\eta_3^2\},\qquad E:\pi_4^2\xrightarrow{\cong}\pi_5^3.
$$

Phase 161 の7規則再構築は、独立に用意された文献由来・完全性由来の葉を要求する限定的な証明構築であり、任意の出典を独立発見するものではない。Phase 162 の `phase162_pi5_3_backward_selection.py` は具体的群構造目標への規則選択を実装するが、一般的な証明発見の完成を意味しない。

主要未解決事項：

- 既存の `ProofStep` ancestry 由来の枝と、新たに必要な部分目標から構築された枝とを区別して記録する。
- 固定された `(5.3)` を Reference として引用した後、そこへ至る Lemma 5.2 等の proof-internal steps を独立の本文根拠として無条件に追加しない。
- Toda 本文の命題掲載順、同一命題内の主張順、各主張が証明済みとなる時点を確認し、証明目標より後にしか得られない結果の参照と自己引用を防ぐ。
- fixed statement と proof-internal fact の分離、循環依存検出、外部葉の provenance は Renderer ではなく proof construction / premise selection に属する。

命題の実際の掲載位置はこの記録から推測しない。`TodaFixedStatementComponent.order` は表示・成分上の順番であり、利用可能な先行証拠であることの証明にはならない。

**記録の性格**：Phase 162 の未解決事項・Phase 163 への引き継ぎであり、上記目標の完全な一般自動証明を認定する記録ではない。2026-10-10 の文書更新で pytest は実行していない。過去の proof records は追記方針で保持した。
'''
}

def update_text(original, addition):
    # Preserve the original complete document; replace only this marked closure section.
    if MARK in original:
        original = original.split('\n' + MARK, 1)[0].rstrip()
    return original.rstrip() + '\n\n' + MARK + '\n\n' + addition.strip() + '\n'

def main():
    if not (ROOT / 'proof.py').exists() or not (ROOT / 'docs').is_dir():
        raise SystemExit('Run from repository root after extraction. proof.py and docs/ must exist.')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = ROOT / f'phase162_docs_backup_{stamp}'
    for rel, addition in SECTIONS.items():
        source = ROOT / rel
        if not source.is_file():
            raise SystemExit(f'Missing current documentation: {rel}')
    for rel, addition in SECTIONS.items():
        source = ROOT / rel
        old = source.read_text(encoding='utf-8-sig')
        dest = backup / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        output = update_text(old, addition)
        source.write_text(output, encoding='utf-8', newline='\n')
        print(f'Updated full document: {rel} ({len(output)} chars)')
    print(f'Backup: {backup}')
    print('pytest NOT run. Source code and tests unchanged.')

if __name__ == '__main__':
    main()
