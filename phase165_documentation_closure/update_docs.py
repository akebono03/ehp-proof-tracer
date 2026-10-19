from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

PHASE_MARKER = '<!-- PHASE165_FINAL_CLOSURE_20261019 -->'
DOCUMENTS = ('README.md', 'docs/design.md', 'docs/development_log.md', 'docs/roadmap.md', 'docs/proof_records.md')
SECTIONS = {
 'README.md': '''## Phase 165 closure (2026-10-19)

**Status: Phase 165 closed after repository-wide test verification.** The final command was `python -m pytest tests -q --tb=short`, with **3,525 passed, 0 failed, and 0 errors** (exit code 0; 21.85 seconds). The run was recorded at `phase165_r6_audit_results/final_pytest/pytest_20261019T104016Z_stdout.txt`, with its accompanying summary and stderr files.

Phase 165 retired historical proof-generation and display pathways in favor of the registered, goal-only, typed backward-search boundary. The production entry point remains fail-closed when an adequately typed goal, vetted citation context, or rule expansion is not configured; a missing proof is never presented as a completed proof. The remaining Phase 164-specific renderer tests were rewritten to verify this boundary, not to revive an old replay implementation.

During the closing regression work, a previous full run collected 3,634 tests and ended with 3,521 passed, 110 failed and 3 errors. The cleanup retired old test functions with backups, corrected the Proposition 5.1 range assertion and beta LaTeX expectation, and narrowed reference selection so that an aggregate fixed statement without an identified component does not automatically become a cited fixed fact. The subsequent final run exercised **3,525 active tests**. Historical tests removed or retired from collection are **not** counted as passing; the change in collection size must not be interpreted as a restored proof capability.

**Scope boundary:** The final passing test suite establishes consistency of the active test set, not that every Toda group has a generally discoverable mathematical proof. In particular, the pi_3^2, pi_4^3, and pi_5^3 end-to-end goal-only proof workflows require separate subsequent verification of source eligibility, registered goals, generator transport, and Narrative output. No repository-wide tests were run solely for this documentation change.
''',
 'docs/design.md': '''## Phase 165 — 旧経路整理と現行探索境界の確定（2026-10-19）

### 設計上の確定事項

- 群別の旧証明選択・旧 Replay・個別 Renderer を、未検証の証明に対する fallback として戻さない。
- 共通 Backward Search（逆向き証明探索）は、型付き Goal（目標）、引用資格を持つ命題識別子、展開規則を必要とする。これらが不足すれば fail-closed（未証明のまま停止）とする。
- Reference（文献固定命題）と Proof Internal（内部導出）を分離する。どの成分か確定できない集約命題を、Reference 選択処理が無条件に昇格させない。
- Presentation / Renderer は既存の証明ステップを表示する責務に限定し、数学的前提の不足を補完しない。

### 完了判定と限界

旧契約に依存するテストをバックアップして退避し、現行契約のテストを保持・更新した。Phase 165 終了時の全体テストは `python -m pytest tests -q --tb=short` で **3525 PASS、FAIL 0、ERROR 0**。これは活動中のテスト集合の整合性を示すもので、退避したテストの合格や、任意群についての証明自動発見を保証しない。次 Phase では個別群の Goal / 出典 / 規則 / 生成元輸送 / 公開 Narrative を現行共通経路で検証する。
''',
 'docs/development_log.md': '''## 2026-10-19 — Phase 165 終了（旧方式整理・全体 pytest PASS）

### 経過

Phase 165 の最終テスト収集で旧方式に依存するエラーが発見され、R6 で旧モジュールと関連テストの整理に移行した。旧機構を再導入せず、退避前のバックアップを保持した。

R6-15 の全体テストは 3634 件を収集し、**3521 PASS / 110 FAIL / 3 ERROR**。失敗ログを根拠に R6-16〜R6-17 で分類し、R6-18 で旧契約由来の失敗105件（96テスト関数、31ファイル）をバックアップのうえ退避した。R6-19 では5ファイルのテストを処理し、関連限定テスト **40 PASS**。R6-20 では `toda_group_proof_narrative_references.py` の `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()` の成分不明な集約 Reference 採用を修正し、限定テスト **26 PASS**。旧入口が十分な Goal と引用命題識別子を持たない場合は、証明済みとせず fail-closed を維持する。

### 最終全体テスト

- 日時：2026-10-19（JST）。
- コマンド：`python -m pytest tests -q --tb=short`
- 結果：**3525 passed in 21.85s**、終了コード 0。
- 標準出力：`phase165_r6_audit_results/final_pytest/pytest_20261019T104016Z_stdout.txt`。
- Summary：`phase165_r6_audit_results/final_pytest/` 配下の最終集計。

### 完了範囲・留保

Phase 165 は、旧実装の依存整理および**現行テスト集合での全体 PASS**をもって終了とする。退避した旧テストを PASS と数えず、過去の Narrative がすべて維持されたとも主張しない。型付き目標からの一般自動証明、Toda 原典のすべての来歴照合、$\\pi_3^2$・$\\pi_4^3$・$\\pi_5^3$ の現行経路での証明生成は後続 Phase の検証対象とする。この文書更新作業では新たな pytest を実行しない。
''',
 'docs/roadmap.md': '''## Phase 165 — 完了（2026-10-19）

旧証明生成・表示経路の直接依存を整理し、現行の型付き Goal-only Backward Search（目標駆動の逆向き証明探索）と fail-closed 境界を維持した。旧方式向けテストをバックアップして退避し、Reference の成分不明な集約命題を自動採用しないよう修正した。

**最終確認：** `python -m pytest tests -q --tb=short` → **3525 PASS、0 FAIL、0 ERROR**（2026-10-19）。退避分は成功したテストに含めない。Phase 165 は現行アクティブテスト集合について完了と判定する。

## 次 Phase — 個別証明の現行共通経路での検証（計画、未着手）

1. $\\pi_3^2$、$\\pi_4^3$、$\\pi_5^3$ の具体的な型付き Goal と出典資格を登録情報から再確認する。
2. Goal-only Backward Search から実際の `ProofStep` が導出できるか、旧アダプターなしで対象ごとに限定検証する。
3. Reference / Proof Internal の分離、生成元の懸垂輸送、Narrative 表示を証明木に基づき確認する。
4. 個別群の未証明状態を隠さない。適用範囲を拡張する場合は次 Phase で計画し、旧方式の fallback を復活させない。

全体 pytest は次 Phase の終了時にのみ実行する。
''',
 'docs/proof_records.md': '''## 2026-10-19 — Phase 165 終了時の証明基盤検証記録

**記録の種類：** 実装・テスト上の境界確認。新しい Toda の数学的命題に対する Proof（証明）登録ではない。

- 旧証明方式に依存するコードとテストをバックアップして整理した。過去のテストを退避した事実は、そのテスト対象の定理が再証明されたことを意味しない。
- Goal-only Backward Search では、目標・引用命題識別子・規則の構成が足りないと `GoalSearchIncompleteError` として停止する。この fail-closed 状態を数学的証明の成立と混同しない。
- `Proposition 5.1` の高次 $\\eta$ 群構造に対する `range_text` の現行期待値は `n >= 3`。Reference フィルターは個別成分未特定の集約命題を無条件で採用しない。
- 全体テストの最終実績は **3525 PASS、FAIL 0、ERROR 0**（2026-10-19）。これは現行のテスト範囲の結果である。

**引継ぎ事項：** $\\pi_3^2$、$\\pi_4^3$、$\\pi_5^3$ の証明を、統一命題台帳・共通規則・出典資格から独立に生成し、生成元輸送および Web Narrative まで確認する必要がある。今回の終了記録はそれらの数学的認証を付与しない。過去の証明記録は消去・上書きせず維持する。
'''
}

def digest(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main()->int:
    root=Path.cwd()
    if not (root/'README.md').is_file() or not (root/'docs').is_dir():
        raise SystemExit('ABORT: run from EHP Proof Tracer repository root')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    base=root/'phase165_documentation_closure_results'/stamp
    backup=base/'backup_full_documents'
    output=base/'updated_full_documents'
    for relative in DOCUMENTS:
        path=root/relative
        if not path.is_file():
            raise SystemExit(f'ABORT: required current document missing: {relative}')
        data=path.read_bytes()
        try: content=data.decode('utf-8-sig')
        except UnicodeDecodeError: raise SystemExit(f'ABORT: non-UTF-8 document: {relative}')
        if PHASE_MARKER in content:
            raise SystemExit(f'ABORT: Phase 165 closure already recorded in {relative}; no changes')
    manifest={}
    for relative in DOCUMENTS:
        path=root/relative
        old=path.read_bytes()
        content=old.decode('utf-8-sig')
        fresh=content.rstrip()+'\n\n'+PHASE_MARKER+'\n\n'+SECTIONS[relative].rstrip()+'\n'
        updated=fresh.encode('utf-8')
        dest=backup/relative; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(old)
        dest=output/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(updated)
        manifest[relative]={'before_sha256':digest(old),'after_sha256':digest(updated),'bytes':len(updated)}
    for relative in DOCUMENTS:
        shutil.copyfile(output/relative,root/relative)
    result={'status':'DOCUMENTATION_UPDATED','phase':'165 closure','files':manifest,'backup':str(backup),'full_files_output':str(output),'full_pytest_rerun':False,'previous_full_pytest':'3525 passed in 21.85s'}
    (base/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
