from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys

MARK = '<!-- PHASE166_HANDOFF_20261021 -->'
TEXT = {
 'README.md': '''

<!-- PHASE166_HANDOFF_20261021 -->
## Phase 166 handoff (2026-10-21)

Phase 166 implementation work is stopped and handed over with an unresolved test-collection boundary. This is **not** a full-suite PASS certification.

The database-backed typed group goal and the public Web adapter were checked in targeted audits. For $\\pi_5^3$, the public Web view rendered the intended goal but returned `generic-partial-proof`, `partial_result=true`, and zero proven steps (R3-AU-12: three targeted tests passed). A displayed goal is not a proof.

Repository-wide pytest attempts were interrupted by historical patch/install modules collected as tests, retired test-helper imports, and Windows command-line length limits. The Phase 165 active test baseline (`python -m pytest tests -q --tb=short`, 3525 passed on 2026-10-19) must not be confused with a Phase 166 whole-repository result.

Phase 167 will first audit and repair the proof narrative for $\\pi_4^3$, then investigate why $\\pi_5^3$ remains partial. See `docs/roadmap.md`, `docs/design.md`, `docs/development_log.md`, and `docs/proof_records.md`.
''',
 'docs/design.md': '''

<!-- PHASE166_HANDOFF_20261021 -->
## Phase 166 終了時の設計境界（2026-10-21）

Phase 166 の開発作業をここで停止する。**全体 pytest 合格による正式な完了認定ではない。** 命題台帳の掲載順、型付き目標、共通探索、公開 Web 表示を結び付けるための限定監査を実施したが、任意の Goal の Proof 完成までは保証しない。

- 群構造データベースから構築した Goal（証明目標）は、証明事実そのものではない。Goal の LaTeX 表示成功と ProofStep の数学的導出を厳密に区別する。
- `generic-complete-proof` は探索結果の完了状態を示すが、日本語 Narrative の意味的な説明・出典対応・重複排除まで保証するとは扱わない。
- `generic-partial-proof` と `partial_result=true` は証明未完成として明示する。$\\pi_5^3$ の Web view は R3-AU-12 で Goal を表示した一方、導出済み ProofStep は0件だった。
- 文献の掲載順による参照可否と、型付き主張の一致・推論規則の適用を混同しない。旧方式の使用順制限や新たな「照合未完了」資格判定は復活させない。
- $\\pi_4^3$ の群構造を既知の数学的前提として用いる場合、別の証明への参照にあたり、その群構造の証明木を必ず再帰的に表示する必要はない。文献固定命題と内部導出の境界は保つ。

Phase 167 では ProofStep と Reference の出自を調べ、共通 Renderer のみ必要最小限修正する。証明本文に規則の内部名を漏らさず、根拠のある日本語説明を生成する。
''',
 'docs/development_log.md': '''

<!-- PHASE166_HANDOFF_20261021 -->
## 2026-10-21 — Phase 166 実装停止・Phase 167 引き継ぎ（全体 pytest 未完了）

### 限定監査の到達点

命題台帳の掲載順、共通 Goal 選択、DB の生成元・群構造を用いた型付き目標の構築、および公開 Web view への接続を段階的に監査した。R3-AU-11 では代表的な群の Goal の LaTeX 生成を確認。R3-AU-12 では $n=3,k=2$、すなわち $\\pi_5^3$ に対し、公開 Flask bridge の view 構築が成功し、`generic-partial-proof` / `partial_result=true` / 本文14行 / `proven_step_count=0` を記録した。R3-AU-12 の限定 pytest は **3 PASS**。これは証明成功の認定ではない。

### Phase 終了時のテスト経緯

全リポジトリ対象の `python -m pytest -q -p no:cacheprovider` は収集途中に `phase165_r6_8_eta_name_fix/install_and_test.py` が `SystemExit` を投げ停止した。続いて `phase165_r6_8_phase58_cutover/install_and_test.py`、`phase165_r6_phase164_migration/apply_and_test.py` のような適用済み変更用スクリプトも pytest の対象となることを確認した。これらは通常のテストではない。

ファイル目録方式ではバックアップの構文エラー2件があり、`BLOCKED_INVENTORY`（2,536候補、37除外）となった。Git 追跡中の候補1,410ファイルを一括実行すると Windows のコマンドライン長上限（エラー206）で起動できなかった。分割実行では最初のバッチにおいて `phase146_7_generic_argument_purpose_prose/test_phase146_7_generic_argument_purpose_prose.py` が削除済みの `tests.test_phase143_19_method_evidence` を import して失敗した。**Phase 166 の全体 PASS は成立していない。**

ユーザーとの合意により、歴史的なテストを無制限に修理・除外する作業を Phase 166 で継続しない。Phase 166 は未解決事項を記録して区切り、全体テスト保証を付与しない。既存本番コードや既存テストを今回の文書更新で変更しない。

### Phase 167 への引き継ぎ

まず $\\pi_4^3$ の Narrative の内部規則名 `infinite cyclic quotient structure`、$\\eta_3=E\\eta_2$ と $E(\\eta_2)=\\eta_3$ の重複、$\\pi_3^2$ の出典対応、$\\pi_4^5=0$ の根拠表示を点検する。その後 $\\pi_5^3$ の partial 探索を Goal / open goals / ProofStep / 引用命題台帳の接続から検証する。旧方式の fallback を復活させず、共通経路を修正する。
''',
 'docs/roadmap.md': '''

<!-- PHASE166_HANDOFF_20261021 -->
## Phase 166 — 実装停止・終了記録（2026-10-21）

- **状態：** 実装作業を終了して次 Phase へ引き継ぐ。全体 pytest 成功による正式完了は**未認定**。
- **実施範囲：** 掲載順を用いる参照候補の探索、DB からの typed Goal 構築、公開 Web adapter 接続の限定監査。
- **残件：** 全体 pytest の現行収集範囲確定、過去の適用スクリプト・旧 helper に依存するテストの整理、$\\pi_4^3$ の文章品質、$\\pi_5^3$ の incomplete な証明探索。

## Phase 167 — 証明修正（次に実施）

1. $\\pi_4^3=\\mathbb Z/2\\{\\eta_3\\}$ の現行 ProofStep / Reference / Web Narrative と関連テストを確認し、数学的導出と公開文章の不足を区別する。
2. 内部推論名 `infinite cyclic quotient structure` の露出、$\\eta_3=E\\eta_2$ と $E(\\eta_2)=\\eta_3$ の重複、$\\pi_3^2$ の出典対応、および $\\pi_4^5=0$ の根拠を、共通 Renderer と証明経路で必要最小限修正する。
3. 対象限定 pytest と公開 Web 表示で正しさを検証する。群別の固定文章や過去方式の fallback を復活させない。
4. $\\pi_5^3$ では表示済み Goal と実際の ProofStep / open goals の差異を調査し、`generic-partial-proof` の原因を特定する。$\\pi_4^3$ の証明木を不要に再帰表示させない。
5. 全体 pytest は Phase 167 の末尾にのみ行う。歴史的テスト整理を証明修正と混同しない。

**補足：** 上記は Phase 165 終了時に記載された「次 Phase（計画）」を現在の実施段階に更新する記録であり、旧履歴は削除しない。
''',
 'docs/proof_records.md': '''

<!-- PHASE166_HANDOFF_20261021 -->
## 2026-10-21 — Phase 166 証明対象・公開 Narrative 監査記録

**記録区分：** 証明インフラと表示の実測。新規数学的定理の Proof（証明）登録ではない。

### $\\pi_4^3$

公開 Web では `generic-complete-proof` と表示され、次の EHP 完全列と第一同型定理による標準的な結論が提示された。

$$
\\pi_5^5\\xrightarrow{\\Delta}\\pi_3^2\\xrightarrow{E}\\pi_4^3\\xrightarrow{H}\\pi_4^5,
$$

$$
\\pi_3^2=\\mathbb Z\\{\\eta_2\\},\\quad
\\Delta(\\iota_5)=\\pm2\\eta_2,\\quad
\\pi_4^5=0,
$$

$$
\\ker E=\\mathbb Z\\{2\\eta_2\\},\\qquad
\\pi_4^3\\cong\\pi_3^2/\\ker E
=\\mathbb Z/2\\{\\eta_3\\}.
$$

数学的な主要導出の表示は確認できるが、内部規則名 `infinite cyclic quotient structure` の残存、$\\eta_3=E\\eta_2$ / $E(\\eta_2)=\\eta_3$ の重複、$\\pi_3^2$ の引用帰属、$\\pi_4^5=0$ の根拠説明の不足がある。`generic-complete-proof` を文章品質完成の保証とみなさない。

### $\\pi_5^3$

R3-AU-12 の公開 Web view 監査で Goal $\\pi_5^3=\\mathbb Z/2\\{\\eta_3^2\\}$ の LaTeX 表示は成功したが、`generic-partial-proof`、`partial_result=true`、導出済み ProofStep 0件だった。限定 pytest は3 PASS。**この時点で証明の完成を認定しない。**

### 留保

Phase 166 の全体 pytest は成功していない。適用用スクリプトの誤収集、バックアップの構文問題、Windows コマンド長上限、消失した旧テスト helper の参照が観測された。個別限定テストの PASS と全体保証を混同しない。Phase 167 の修正では原典・登録済み Reference と現行 ProofStep を照合し、実際の推論のない表示だけを証明済みとしない。
'''
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    targets = {root / name: content for name,content in TEXT.items()}
    missing = [str(p) for p in targets if not p.is_file()]
    if missing:
        print('ABORT: missing source documents:', *missing, sep='\n', file=sys.stderr)
        return 2
    old = {}
    for p in targets:
        data = p.read_bytes()
        if MARK.encode('utf-8') in data:
            print('ABORT: marker already exists; refusing duplicate update:',p,file=sys.stderr)
            return 2
        old[p] = data
    out = root / 'phase166_docs_closure_output' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out.mkdir(parents=True, exist_ok=False)
    manifest=[]
    for p, appendix in targets.items():
        rel = p.relative_to(root)
        original = old[p].decode('utf-8-sig')
        backup = out / 'backup' / rel
        updated = out / 'full_documents' / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        updated.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(old[p])
        # Keep all old content verbatim (except a possible UTF-8 BOM) and append the dated canonical handoff.
        text = original.rstrip('\r\n') + '\n' + appendix
        updated.write_text(text, encoding='utf-8')
        manifest.append({'file':rel.as_posix(),'original_sha256':hashlib.sha256(old[p]).hexdigest(),'full_output':str(updated),'backup':str(backup)})
    # Prepare all outputs before applying any file.
    for p in targets:
        rel = p.relative_to(root)
        shutil.copyfile(out / 'full_documents' / rel, p)
        print('UPDATED:',rel,'FULL:',out / 'full_documents' / rel)
    (out / 'manifest.json').write_text(json.dumps({'phase':'166','next_phase':'167','status':'HANDOFF_WITH_FULL_PYTEST_UNRESOLVED','production_code_modified':False,'tests_run':False,'documents':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('DOCUMENTS_OUTPUT:',out)
    print('NO PYTEST RUN; no production code or tests changed')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
