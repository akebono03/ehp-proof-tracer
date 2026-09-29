from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(".")
OUT = Path("phase145_documentation_closure") / "updated_full_documents"

FILES = {
    "README.md": ROOT / "README.md",
    "design.md": ROOT / "docs" / "design.md",
    "development_log.md": ROOT / "docs" / "development_log.md",
    "roadmap.md": ROOT / "docs" / "roadmap.md",
    "proof_records.md": ROOT / "docs" / "proof_records.md",
}


README_CLOSURE = r"""
## Phase 145 closure

Phase 145 intentionally kept its functional scope narrow: it changed the default
group-proof presentation to Narrative at depth 2 without changing proof semantics,
stored provenance, theorem facts, or explicit user selections.

The default CLI behavior is now equivalent to:

```powershell
python main.py group-proof n k --mode narrative --depth 2
```

Explicit selections remain available:

```powershell
python main.py group-proof 9 7 --mode trace --depth 0
python main.py group-proof 9 7 --mode outline --depth 1
python main.py group-proof 9 7 --mode narrative --depth 2
```

The Web group-proof form likewise defaults to Narrative and depth 2 while preserving
the existing Trace / Outline / Narrative and depth 0 / 1 / 2 choices.

Phase 145 also completed repository cleanup by moving historical Phase artifacts under
`archive/phases/`. The cleanup exposed mixed canonical-test import conventions:
some tests import `tests.test_*`, while older tests import bare `test_*` modules.
The final compatibility repair preserves both conventions with an explicit
`tests` package marker and a test-only import compatibility layer. Production code
and existing canonical test bodies were not changed for that repair.

Phase 145 focused regression:

```text
46 passed in 15.62s
```

Canonical collection after the compatibility repair:

```text
10303 tests collected
```

Final repository-wide regression:

```text
10303 passed in 2375.31s (0:39:35)
```

Phase 145 does not implement result reuse, new Narrative generalization rules,
new theorem facts, or new proof search. From Phase 146 onward, one concrete
generalization issue is handled per Phase with the minimum general rule needed for
that issue.
"""


DESIGN_CLOSURE = r"""
# 29. Phase 145 完了境界

Phase 145 の機能変更は group-proof の default presentation だけである。

```text
default mode
→ Narrative

default depth
→ 2
```

CLI の default は概念的に次と同値である。

```powershell
python main.py group-proof n k --mode narrative --depth 2
```

Web group-proof も同じ default を使用する。

明示指定は従来どおり維持する。

```text
--mode trace
--mode outline
--mode narrative

--depth 0
--depth 1
--depth 2
```

したがって:

```text
default presentation change
!= replay semantics change
!= proof graph change
!= proof provenance change
!= theorem fact change
!= new proof search
```

Phase 145 の repository cleanup では historical Phase artifact を
`archive/phases/` 以下へ整理した。

cleanup 後の canonical test collection で、既存 test suite に

```text
tests.test_* package import
bare test_* import
```

の2形式が共存していることを確認した。

最終的な test-only compatibility boundary は:

```text
tests/__init__.py
→ tests package を明示

tests/conftest.py
→ tests directory を import path に追加
```

である。

これは既存 canonical test 本体の大量書き換えを避けるための test infrastructure であり、
production import semantics を変更しない。

Phase 145 focused regression:

```text
46 passed in 15.62s
```

canonical collection:

```text
10303 tests collected
```

repository-wide final:

```text
10303 passed in 2375.31s (0:39:35)
```

Phase 145 完了。

Phase 146 以降は1 Phase につき1つの concrete issue を選び、その issue に必要な
最小一般規則だけを追加する。

```text
one concrete issue
→ minimum general rule
→ focused regression
→ existing proof preservation
```

Phase 145 では result-reuse、追加の ownership model、将来 proof のためだけの
semantic rule、一般 evaluator は実装していない。
"""


DEVLOG_CLOSURE = r"""
---

# Phase 145 — Narrative + depth 2 default / repository closure

Phase 145 は Phase 144 後の表示 default を確定するための狭い Phase とした。

機能上の目的:

```text
group-proof default mode
trace → narrative

group-proof default depth
→ 2
```

新しい theorem fact、proof search、Narrative generalization は追加していない。

## default presentation

CLI parser と group-proof execution path の default を

```text
mode = narrative
depth = 2
```

へ変更した。

Web group-proof form / adapter も同じ default に変更した。

既存の explicit selection:

```text
trace / outline / narrative
depth 0 / 1 / 2
```

は維持した。

legacy test が Trace 自体を検証する箇所では `--mode trace` または
`group_proof_mode=trace` を明示し、default 変更と Trace semantics の検証を分離した。

focused regression:

```text
46 passed in 15.62s
```

## repository cleanup

historical Phase artifact を `archive/phases/` 以下へ整理した。

cleanup 後の whole-suite collection では canonical test が archived helper / historical
test helper に依存していた箇所が表面化したため、必要な canonical dependency を復元した。

その後、canonical tests 自体に2種類の import style が共存していることを確認した。

R7 inventory:

```text
canonical test files: 774
tests.test_* package imports: 43
bare test_* imports: 547
unique bare test_* modules: 184
bare modules without canonical target: 0
```

547箇所の既存 import を書き換えず、test infrastructure のみで互換性を維持した。

追加:

```text
tests/__init__.py
tests/conftest.py
```

`tests/conftest.py` は `tests/` directory を test execution 時の import path に追加する。
production code は変更しない。

R8 canonical collection:

```text
10303 tests collected
```

R8 focused regression:

```text
46 passed in 15.62s
```

## final repository-wide regression

Phase 最後にのみ実行:

```powershell
python -m pytest tests -q
```

結果:

```text
10303 passed in 2375.31s (0:39:35)
```

fail / collection error は0件。

## Phase 145 completion boundary

```text
Narrative default
depth 2 default
explicit mode/depth compatibility preserved
historical Phase artifact archive cleanup
canonical test import compatibility restored
production proof semantics unchanged
10303 repository-wide tests PASS
```

Phase 145 完了。

Phase 146 以降は一般化不足を一括処理せず、

```text
1 Phase
→ 1 concrete issue
→ minimum general rule
→ focused regression
```

の順で進める。
"""


ROADMAP_REPLACEMENT = r"""## Phase 145 — 完了

Phase 145 の目的は次の default presentation change に限定した。

```text
group-proof default mode
trace → narrative

group-proof default depth
→ 2
```

CLI / Web の default を Narrative + depth 2 に変更し、explicit user selection の
Trace / Outline / Narrative および depth 0 / 1 / 2 は維持した。

Phase 145 では次を実装していない。

```text
result-reuse の一般化
ownership model の追加変更
新しい semantic statement type の先回り実装
新しい theorem fact
新しい proof search
general E/H/Delta evaluator
```

repository cleanup 後に canonical test import dependency を修復し、mixed import style
に対する test-only compatibility layer を追加した。

最終 repository-wide regression:

```text
10303 passed in 2375.31s (0:39:35)
```

Phase 145 完了。

## Phase 146 以降 — 1 Phase = 1 concrete issue

Phase 146 以降は「一般化を先に完成させる」方式を採用しない。

基本手順:

```text
1. 次に通したい具体的な証明を1つ選ぶ
2. generic Narrative で不足している具体的課題を1つ特定する
3. その課題だけを解く最小一般規則を設計する
4. target-specific special case を作らず実装する
5. focused regression で既存証明を守る
6. その Phase を閉じる
```

各 Phase の完了条件:

> 対象となる1課題を target-specific special handling ではなく一般規則で解決し、
> 既存の証明を壊さない。

例:

```text
ある具体的 proof で Reference reuse だけが不足
→ その Phase は Reference reuse だけ

次の proof で composition expression が不足
→ 次 Phase は composition expression だけ

result-reuse が初めて具体的 blocker になる
→ その Phase で result-reuse の最小一般規則だけ
```

巨大な「すべての一般規則を完成させる Phase」は作らない。
"""


PROOF_CLOSURE = r"""
---

# Phase 145 default presentation / regression provenance record

Phase 145 は数学的 proof provenance を変更した Phase ではない。

目的は、Phase 144 までに構築した group-result Narrative を通常利用時の default
presentation とすることだった。

## default presentation boundary

default:

```text
mode = Narrative
depth = 2
```

explicit selection:

```text
Trace / Outline / Narrative
depth 0 / 1 / 2
```

は維持する。

```text
default mode change
!= ProofStep change

default depth change
!= proof ancestry change

Narrative default
!= Narrative theorem inference
```

Phase 145 の default depth 2 は user-facing initial selection であり、
既存 complete replay / bounded replay semantics を別物へ変更するものではない。

## repository cleanup provenance boundary

historical Phase artifact は `archive/phases/` 以下へ整理した。

canonical tests が必要とする test helper / audit helper は archive-only artifact と
同一視せず、canonical dependency として利用可能な状態を維持する。

cleanup 後の import regression は数学的 provenance の failure ではなく test collection
infrastructure の compatibility problem だった。

確認した mixed import inventory:

```text
tests.test_* package imports: 43
bare test_* imports: 547
unique bare test_* modules: 184
bare modules without canonical target: 0
```

最終 test-only compatibility:

```text
tests/__init__.py
tests/conftest.py
```

production proof repository、`ProofStep`、Narrative renderer の数学的 semantics は変更していない。

## final verification record

focused:

```text
46 passed in 15.62s
```

canonical collection:

```text
10303 tests collected
```

repository-wide final:

```text
10303 passed in 2375.31s (0:39:35)
```

したがって Phase 145 の provenance boundary は:

```text
Narrative + depth 2 default
+
repository/test infrastructure closure
```

であり、

```text
new theorem fact
new proof edge
new proof search
new Narrative generalization rule
result-reuse framework
```

は含まない。

Phase 146 以降は concrete proof pressure を1件ずつ選び、その不足に必要な最小一般規則だけを
追加する。
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def replace_once_required(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def update_readme(text: str) -> str:
    text = text.replace(
        "The default mode is `trace`, preserving Phase 131 behavior.",
        "The default mode is `narrative` and the default depth is `2`. "
        "Trace and Outline remain available through explicit selection.",
    )
    text = text.replace(
        "- Web group-proof display with selectable depth 0, 1, or 2 and Trace / Outline / Narrative modes,",
        "- Web group-proof display defaulting to Narrative at depth 2, with selectable depth 0, 1, or 2 and Trace / Outline / Narrative modes,",
    )
    text = text.replace(
        "Latest canonical repository-wide Phase 144 run:",
        "Historical canonical repository-wide Phase 144 run:",
    )
    return append_once(text, "## Phase 145 closure", README_CLOSURE)


def update_design(text: str) -> str:
    text = text.replace(
        "`--mode` 省略時は `trace`。\n\n既存 Phase 131 semantics を維持する。",
        "`--mode` 省略時は `narrative`、`--depth` 省略時は `2`。\n\n"
        "Trace / Outline / Narrative と depth 0 / 1 / 2 の明示指定 semantics は維持する。",
    )
    text = text.replace(
        "default:\n\n```text\ntrace\n```\n\nPhase 131 compatibility を維持。",
        "default:\n\n```text\nNarrative\nDepth 2\n```\n\n"
        "Trace / Outline / Narrative と depth 0 / 1 / 2 の explicit selection は維持する。",
    )
    return append_once(text, "# 29. Phase 145 完了境界", DESIGN_CLOSURE)


def update_development_log(text: str) -> str:
    return append_once(text, "# Phase 145 — Narrative + depth 2 default / repository closure", DEVLOG_CLOSURE)


def update_roadmap(text: str) -> str:
    start = text.find("## Phase 145 — default presentation change only")
    end = text.find("## 先取りしないもの", start)
    if start == -1 or end == -1:
        if "## Phase 145 — 完了" in text:
            return text
        raise RuntimeError("roadmap.md: Phase 145 planned section boundary not found")
    return text[:start] + ROADMAP_REPLACEMENT.strip() + "\n\n" + text[end:]


def update_proof_records(text: str) -> str:
    return append_once(text, "# Phase 145 default presentation / regression provenance record", PROOF_CLOSURE)


UPDATERS = {
    "README.md": update_readme,
    "design.md": update_design,
    "development_log.md": update_development_log,
    "roadmap.md": update_roadmap,
    "proof_records.md": update_proof_records,
}


def main() -> int:
    missing = [str(path) for path in FILES.values() if not path.is_file()]
    if missing:
        raise RuntimeError("Missing required document(s): " + ", ".join(missing))

    OUT.mkdir(parents=True, exist_ok=True)

    for name, path in FILES.items():
        original = read(path)
        updated = UPDATERS[name](original)
        write(path, updated)
        write(OUT / name, updated)
        print(f"Updated full document: {path}")
        print(f"Copied full document: {OUT / name}")

    print()
    print("Phase 145 documentation closure: PASS")
    print("Production code changes: none")
    print("Test code changes: none")
    print("Repository-wide pytest: not rerun; Phase 145 final run already passed 10303 tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
