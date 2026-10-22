from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil

DOCS = (
    Path("docs/development_log.md"),
    Path("docs/proof_records.md"),
    Path("docs/roadmap.md"),
)
MARKER = "<!-- PHASE167_CLOSURE_20261022 -->"

DEVELOPMENT = r"""
<!-- PHASE167_CLOSURE_20261022 -->
## 2026-10-22 — Phase 167 終了（1-stem 共通証明・Reference 接続）

### 完了した範囲

- 現行共通 Backward Search / Renderer による 1-stem の公開 Narrative を監査した。$n=2$ から $31$ の30群で `complete=True`、監査指摘0件を確認した。これは監査した範囲の結果であり、その他の stem の完成を主張しない。
- Toda (5.1) の一般形を Reference、特殊化結果を Proof に表示する共通接続を調整した。$\pi_4^3$ の証明では同じ `[R1]` が $\pi_5^5=\mathbb Z\{\iota_5\}$ と $\pi_4^5=0$ の両方に接続することを確認した。零群専用の Renderer 分岐は採用しない。
- Toda (4.5) の一般形と 1-stem 安定輸送の本文表示を確認した。Proposition 5.1 から使用する $\pi_4^3$ の群構造を参照し、完成証明木そのものを再表示しない。
- Proposition 4.2 の EHP 完全列は Reference に列記せず、Proof 本文に必要な完全列を1本表示する既定方針を維持した。
- Phase 167 R5 で、ギリシャ文字 $\beta$ のテスト期待値のみを二重バックスラッシュから通常の `\beta` に訂正。対応する限定 pytest は1 PASS。本番のギリシャ文字変換コードは変更していない。

### Phase 終了時の全体 pytest

- 実行日：2026-10-22（JST）。
- 実行コマンド：`python -m pytest tests -q --tb=short --disable-warnings --ignore=tests/test_phase144_6_pi6_generic_production_route.py --ignore=tests/test_phase144_6_public_route_cutover.py`
- 結果：**3543 passed in 25.68s**、FAIL 0、ERROR 0、終了コード 0。
- 実行ログ：`phase167_closure_rerun/pytest_full.log`。
- 2つの `--ignore` 対象は Phase 165 で退避対象とされた、削除済み `tests.test_phase143_19_method_evidence` に依存する旧 Phase 144 テストである。これらを PASS 件数に含めない。
- リポジトリ全体を無制限に収集した過去の試行は旧インストールスクリプトの `SystemExit` で停止しており、上記結果は現行 `tests` の指定範囲に対するものとする。

### Phase 168 への引き継ぎ

次工程は 2-stem の Backward Search による証明生成。最初の対象 $\pi_5^3=\mathbb Z/2\{\eta_3^2\}$ は現行公開経路では `generic-partial-proof` であり、Phase 167 で完成を認定していない。既存の命題台帳、ProofStep、文献掲載順と生成元懸垂輸送の接続を監査し、必要な推論規則を判断する。1-stem の証明表示経路は不要に変更しない。
""".strip()

PROOF = r"""
<!-- PHASE167_CLOSURE_20261022 -->
## 2026-10-22 — Phase 167 1-stem 証明生成・Reference 表示検証

**記録区分：** 既存文献と ProofStep に基づく証明生成・表示の検証であり、新しい数学的定理の発見を主張するものではない。

公開 1-stem について $n=2,\ldots,31$ の30群で完成証明が表示され、監査指摘0件だった。

$\pi_4^3$ の代表例では、Toda (5.1) を次の一般命題として Reference に掲載する。

$$
\pi_i^n=0\quad(i<n),\qquad \pi_n^n=\mathbb Z\{\iota_n\}\quad(n\ge1).
$$

証明本文では既存の特殊化 ProofStep の依存関係に従い、同じ `[R1]` から以下を得る。

$$
\pi_5^5=\mathbb Z\{\iota_5\},\qquad \pi_4^5=0.
$$

EHP 完全列（Proposition 4.2）は Reference に重複掲示せず、証明本文に1本表示する。Proposition 5.1 の $\Delta(\iota_5)=\pm2\eta_2$ と $\pi_3^2=\mathbb Z\{\eta_2\}$ を用い、核と全射性から $\pi_4^3=\mathbb Z/2\{\eta_3\}$ の表示を確認した。

$n\ge4$ の 1-stem は、Toda (4.5) による安定輸送と $\pi_4^3$ の群構造の利用を公開表示で確認した。すべての一般命題について数学的な正しさを個別に再証明したという意味ではない。

**回帰結果：** 2026-10-22、現行 `tests` の指定範囲に対する pytest は 3543 PASS、FAIL 0、ERROR 0。削除済み旧 helper に依存する旧テスト2ファイルは明示除外。Phase 168 では未完成の 2-stem（最初の対象 $\pi_5^3$）を扱い、この完了実績に混同しない。
""".strip()

ROADMAP = r"""
<!-- PHASE167_CLOSURE_20261022 -->
## Phase 167 — 完了（2026-10-22）

**完了範囲：** 1-stem（$n=2$〜$31$、$k=1$）の30群すべてで現行公開 Narrative の `complete=True` と監査指摘0件を確認した。Toda (5.1) の一般形／特殊化結果の Reference 接続、Toda (4.5) の安定輸送の表示、Proposition 4.2 の完全列を Reference に入れず本文に1本表示する方針を維持した。

**Phase 終了時全体 pytest：** `python -m pytest tests -q --tb=short --disable-warnings --ignore=tests/test_phase144_6_pi6_generic_production_route.py --ignore=tests/test_phase144_6_public_route_cutover.py` → **3543 PASS、FAIL 0、ERROR 0**（2026-10-22、終了コード0）。除外2件は削除済みの旧 helper に依存する Phase 165 退避対象であり、PASS に算入しない。

## Phase 168 — 2-stem 証明生成（次工程・未着手）

1. 最初の対象 $\pi_5^3=\mathbb Z/2\{\eta_3^2\}$ の現行 `generic-partial-proof` と未解決 Goal を監査する。
2. 命題台帳と原典掲載順に基づき、使用可能な既存 Reference・型付き推論規則・ProofStep を確認する。旧方式の完成証明・固定文章は導入しない。
3. $E(\eta_2^2)=\eta_3^2$ 等の生成元輸送について、実際の前提と数学的な推論の有無を調べる。
4. 2-stem の実証が得られた範囲だけ完成と記録する。1-stem の共通経路を不必要に改変しない。
5. 全体 pytest は Phase 168 の終了時に実施する。
""".strip()


def main() -> None:
    root = Path.cwd().resolve()
    paths = [root / relative for relative in DOCS]
    if not all(p.is_file() for p in paths):
        raise RuntimeError("Run in the repository root with docs/ files available")
    contents = {p: p.read_text(encoding="utf-8-sig") for p in paths}
    already = [MARKER in contents[p] for p in paths]
    if any(already):
        if all(already):
            print("ALREADY_APPLIED: All Phase 167 closure records are present")
            return
        raise RuntimeError("Partial closure markers found; inspect documents before applying")
    if not all("Phase 166" in contents[p] for p in paths):
        raise RuntimeError("Expected Phase 166 context missing")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = root / "phase167_documentation_closure_output" / stamp
    backup = output / "backup_full_documents"
    full = output / "updated_full_documents"
    for path in paths:
        rel = path.relative_to(root)
        (backup / rel).parent.mkdir(parents=True, exist_ok=True)
        (full / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup / rel)
    additions = dict(zip(paths, (DEVELOPMENT, PROOF, ROADMAP)))
    for path in paths:
        updated = contents[path].rstrip() + "\n\n" + additions[path] + "\n"
        (full / path.relative_to(root)).write_text(updated, encoding="utf-8", newline="\n")
    for path in paths:
        shutil.copy2(full / path.relative_to(root), path)
        print("UPDATED:", path)
        print("FULL_DOCUMENT:", full / path.relative_to(root))
    result = {
        "phase": 167,
        "status": "DOCUMENTATION_UPDATED",
        "scope": "1-stem n=2..31, k=1",
        "audit": "30 complete, 0 findings",
        "pytest": "3543 passed in 25.68s, 0 failed, 0 errors; 2 retired legacy files ignored",
        "backup": str(backup),
        "full_documents": str(full),
        "tests_run_by_this_script": False,
        "phase168_status": "planned, not started",
    }
    (output / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REPORT:", output / "report.json")


if __name__ == "__main__":
    main()
