from __future__ import annotations

import ast
import subprocess
from pathlib import Path


ARCHIVE_ROOT = Path("archive/phases")
TESTS_ROOT = Path("tests")


def git_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path.as_posix()],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def desired_path(module: str) -> Path | None:
    if module.startswith("tests."):
        parts = module.split(".")
        if len(parts) == 2:
            return TESTS_ROOT / f"{parts[1]}.py"
        return None

    if module.startswith("audit_phase"):
        return Path(f"{module}.py")

    return None


def archive_candidates(target: Path) -> list[Path]:
    name = target.name
    candidates = [
        path
        for path in ARCHIVE_ROOT.rglob(name)
        if path.is_file() and git_tracked(path)
    ]
    return sorted(candidates, key=lambda p: p.as_posix())


def choose_candidate(target: Path, candidates: list[Path]) -> Path:
    if len(candidates) == 1:
        return candidates[0]

    if target.parent == Path("."):
        root_file = ARCHIVE_ROOT / "_root_files" / target.name
        if root_file in candidates:
            return root_file

    suffix = target.as_posix()
    suffix_matches = [
        path for path in candidates
        if path.as_posix().endswith("/" + suffix)
    ]
    if len(suffix_matches) == 1:
        return suffix_matches[0]

    raise RuntimeError(
        "Ambiguous archived dependency for "
        f"{target}: {[p.as_posix() for p in candidates]}"
    )


def discover_direct_missing_dependencies() -> dict[Path, Path]:
    missing: dict[Path, Path] = {}

    for test_path in sorted(TESTS_ROOT.glob("test_*.py")):
        for module in imported_modules(test_path):
            target = desired_path(module)
            if target is None or target.exists():
                continue

            candidates = archive_candidates(target)
            if not candidates:
                raise RuntimeError(
                    f"Missing canonical dependency {module} -> {target}; "
                    "no tracked archived source found"
                )

            source = choose_candidate(target, candidates)
            previous = missing.get(target)
            if previous is not None and previous != source:
                raise RuntimeError(
                    f"Conflicting archived sources for {target}: "
                    f"{previous} and {source}"
                )
            missing[target] = source

    return missing


def restore_with_git_mv(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", source.as_posix(), target.as_posix()],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(
            f"git mv failed: {source} -> {target}\n{detail}"
        )


def main() -> int:
    if not ARCHIVE_ROOT.is_dir():
        raise RuntimeError("archive/phases not found")
    if not TESTS_ROOT.is_dir():
        raise RuntimeError("tests not found")

    missing = discover_direct_missing_dependencies()

    print(f"Direct missing canonical dependencies: {len(missing)}")
    if not missing:
        print("No direct archived dependencies need restoration.")
        print("Phase 145 Final Regression Repair R1 apply: PASS")
        return 0

    print("Restoring canonical test dependencies:")
    for target, source in sorted(
        missing.items(), key=lambda item: item[0].as_posix()
    ):
        print(f"  {source} -> {target}")
        restore_with_git_mv(source, target)

    remaining = discover_direct_missing_dependencies()
    if remaining:
        raise RuntimeError(
            "Direct missing dependencies remain after restoration: "
            + ", ".join(path.as_posix() for path in remaining)
        )

    print("Phase 145 Final Regression Repair R1 apply: PASS")
    print(f"Restored modules: {len(missing)}")
    print("Production code changes: none")
    print("Existing test bodies/imports changed: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
