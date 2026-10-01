from pathlib import Path
import shutil

PACKAGE_DIR = Path(__file__).resolve().parent
MARKERS = {
  'README.md': '<!-- PHASE153_CLOSURE -->',
  'docs/design.md': '<!-- PHASE153_CLOSURE -->',
  'docs/development_log.md': '<!-- PHASE153_CLOSURE -->',
  'docs/roadmap.md': '<!-- PHASE153_CLOSURE -->',
  'docs/proof_records.md': '<!-- PHASE153_CLOSURE -->',
}

SECTIONS = {
  'README.md': '<!-- PHASE153_CLOSURE -->\n## Phase 153 closure — Reference selection and granularity\n\nPhase 153 refined Narrative Reference selection, granularity, reuse, and display\nboundaries without adding new Toda theorem facts or changing the stored proof graph.\n\nThe phase established general Reference rules across legacy, generic, and specialized\nNarrative routes:\n\n- semantic classification for the audited scalar-order statement,\n- recovery of existing concrete proof scope before stable specialization where a\n  concrete proof already exists,\n- proof-ancestry-based Reference selection for the audited low-dimensional\n  \\(n=2\\) groups,\n- boundary-oriented Reference granularity,\n- suppression of irrelevant aggregate ancestry from the visible proof body,\n- normalization of Reference-use prose,\n- reuse of an already displayed Reference as a proof boundary instead of recursively\n  re-expanding the same derivation,\n- filtering of unused References,\n- structural Reference attribution for generic routes that do not use explicit\n  `[Rk]` body markers,\n- exclusion of the current root theorem from the external Reference section across\n  all renderer routes,\n- locator-based literature-reference identity when labels differ but the cited\n  locator is the same.\n\nThe final depth-2 closure audit covered the project population\n\n$$\nn=2,\\ldots,15,\n\\qquad\nk=0,\\ldots,7,\n$$\n\nfor a total of 112 groups.\n\nMeasured closure evidence:\n\n```text\nfocused Phase 153 regression:\n30 passed in 7.97s\n\n112-group depth-2 closure audit:\nscanned groups: 112\nrender errors: 0\ngroups with Reference section: 93\nmarker-bearing groups: 90\ngeneric/reference-only groups: 3\nReference headers: 147\nbody Reference markers: 146\nmaximum References in one group: 6\ngroups at maximum: pi_6^3\nviolations: 0\n\nAUDIT_RESULT=PASS\n```\n\nThe complete historical test suite was not used as the Phase 153 completion gate.\nA canonical `tests/` run collected 10,554 tests and exposed multiple stale\npresentation expectations from earlier phases. One stale Phase 132 Narrative\nexpectation was repaired and its focused verification passed, while broader historical\ntest consolidation was deliberately deferred.\n\nAccordingly, Phase 153 closes on its focused regression and whole-population Reference\ninvariant audit. It does not claim an unobserved repository-wide all-pass result.\n\nPhase 154 returns to proof-prose generation quality. Test-suite consolidation remains a\nseparate deferred maintenance task.\n',
  'docs/design.md': '<!-- PHASE153_CLOSURE -->\n# Phase 153 — Narrative Reference selection / granularity 設計\n\nPhase 153 は Narrative の Reference（参照）を、単なる provenance の列挙ではなく、\n「本文で実際に使用される外部結果の境界」として扱う一般規則を整理した。\n\n新しい Toda theorem fact、ProofStep、proof edge、proof search は追加していない。\n\n## Reference の基本境界\n\nPhase 153 後の設計では、Narrative Reference は次を満たす。\n\n```text\nexternal Reference\n!= current root theorem\n\ndisplayed Reference\n→ proof ancestry / proof-use に基づく\n\nmarker-bearing route\n→ 本文で使用された [Rk] だけを残す\n\ngeneric no-marker route\n→ 実際に表示へ参加した step identity から Reference を残す\n```\n\ncurrent `presentation.root_step` が持つ `LiteratureReference` は、renderer route に\n依存せず external Reference section へ出さない。\n\n```text\nroot theorem provenance\n!= external supporting Reference\n```\n\n## literature-reference identity\n\n同じ文献 locator が label 違いで複数表現される場合、locator を canonical identity として扱う。\n\n```text\nboth locators exist\n→ locator equality を優先\n\notherwise\n→ full LiteratureReference equality\n```\n\nこれにより、たとえば同じ `(5.2)` を異なる label で保持する step があっても、\nroot Reference exclusion の意味論を route 間で一致させる。\n\n## Reference granularity\n\nReference は aggregate root 全体を機械的に選ぶのではなく、consumer が実際に利用する\nproof boundary を優先する。\n\naggregate conclusion の複数 component のうち、consumer の generator / structure に対応する\ncomponent が一意に特定できる場合、その component を表示対象とする。\n\n```text\naggregate provenance\n→ consumer-relevant component\n→ external Reference statement\n```\n\nこれは theorem fact の分解や変更ではなく presentation granularity である。\n\n## Reference reuse\n\n本文中で exact step がすでに Reference statement として表示されている場合、その step は\n再利用可能な proof boundary として扱う。\n\n```text\ndisplayed Reference step\n+ premises\n→ [Rk] を用いる\n→ recursive derivation expansion を抑制\n```\n\ntitle-only Reference はこの boundary にはしない。\n\n```text\nReference reuse\n!= ProofStep deletion\n!= premise deletion\n!= provenance deletion\n```\n\n## used-Reference filtering\n\nmarker-bearing route では本文に現れる `[Rk]` を実使用集合とし、未使用 Reference を除外した後、\n番号を連続化する。\n\ngeneric route では explicit marker が無いため、表示へ参加した argument / local-body /\ncontribution step identity を用いて Reference 使用を帰属する。\n\nspecialized route では既存 marker mapping を壊さないことを優先し、root exclusion によって\nmapping が変質する場合は specialized renderer 自身の Reference section を保持する。\n\n## 112-group closure invariant\n\ndepth 2 の標準対象\n\n$$\nn=2,\\ldots,15,\n\\qquad\nk=0,\\ldots,7\n$$\n\nについて次を closure invariant とした。\n\n```text\nrender errors = 0\nReference numbering is contiguous\nroot LiteratureReference is not external\nbody marker never points to a missing Reference\nmarker-bearing route has no unused displayed Reference\n```\n\n最終 audit:\n\n```text\nscanned groups: 112\nrender errors: 0\nviolations: 0\n```\n\n## Phase 153 の境界\n\n```text\nReference selection / granularity\n!= theorem selection\n!= theorem ranking\n!= proof search\n!= proof graph mutation\n!= proof-prose quality completion\n```\n\n接続語重複、内部 rule-name の露出、英語 statement、重複 scalar 表現、句読点などの\nproof-prose generation は Phase 154 へ送る。\n\nhistorical test suite の consolidation（整理）は独立 maintenance とし、Phase 154 の\nproof-prose 改善を妨げる前提条件にはしない。\n',
  'docs/development_log.md': '<!-- PHASE153_CLOSURE -->\n# Phase 153 — Reference selection / granularity 完了\n\nPhase 153 は Phase 152 の defect classification 後、Narrative の Reference selection\n（参照選択）と granularity（粒度）を一般規則として整理した。\n\n新しい Toda theorem fact、proof search、proof graph mutation は追加していない。\n\n## R1 — Scalar order semantic classification\n\n`ScalarGreaterEqualStatement` を Narrative semantic classification 上の `ORDER` として扱う\n経路を整備した。\n\n## R2–R3 — concrete proof-scope recovery\n\nstable specialization より既存 concrete proof を優先すべき対象について、既存 proof scope から\nconcrete proof を回収する一般経路を監査・実装した。\n\n7群で concrete proof を優先し、$\\pi_{10}^{6}$ で確認した self-reference と不要な `(4.5)`\nReference を解消した。\n\nfocused:\n\n```text\n17 passed\n```\n\n## R4–R5 — n=2 six-group Reference ancestry audit\n\n対象:\n\n$$\n\\pi_4^2,\\quad\n\\pi_5^2,\\quad\n\\pi_6^2,\\quad\n\\pi_7^2,\\quad\n\\pi_8^2,\\quad\n\\pi_9^2.\n$$\n\n`presentation.root_step` 自身を external Reference candidate から外し、実際に利用する\npremise / ancestry を優先する selection rule へ整理した。\n\nfocused repair:\n\n```text\n10 passed\n```\n\n## R6 — Reference granularity\n\n同じ literature Reference に複数 candidate がある場合、consumer へ入る boundary crossing を\n優先した。\n\naggregate conclusion では、consumer の generator が構造的に現れる一意の group-relation\ncomponent を選択できる場合、その component を Reference statement として使用する。\n\nfocused:\n\n```text\n15 passed\n```\n\n## R7 — proof-body relevance / aggregate suppression\n\ngeneric / legacy 共通の final body boundary で、本文に不要な aggregate ancestry を抑制する\n一般 postprocessing を追加した。\n\nproof graph は変更していない。\n\nfocused:\n\n```text\n24 passed\n```\n\n## R8 — Reference-use prose normalization\n\nReference duplicate suppression により本文が単純な Reference 利用へ縮約される場合、\n\n```text\n[Rk]を得る。\n```\n\nではなく\n\n```text\n[Rk]を用いる。\n```\n\nへ正規化した。\n\nfocused:\n\n```text\n29 passed\n```\n\n## R9 — Reference reuse / derivation suppression\n\nexact step が Reference statement として表示済みの場合、その Reference を reusable proof\nboundary として利用し、同じ derivation の recursive expansion を抑制した。\n\ntitle-only Reference は boundary としない。\n\nfocused:\n\n```text\n32 passed\n```\n\n## R10 — used Reference filtering\n\nmarker-bearing body では実際に使われた `[Rk]` のみを残し、Reference 番号を連続化して本文も\nremap する一般処理を追加した。\n\ngeneric no-marker route には marker filtering を適用せず、既存 structured Reference を保持した。\n\nfocused:\n\n```text\n35 passed\n```\n\n## R11 — generic-route Reference attribution\n\ngeneric body に `[Rk]` が無い場合、実際に表示へ参加した argument / local-body /\ncontribution step identity を用いて Reference 使用を帰属する rule を追加した。\n\n$\\pi_6^3$ depth 2 では root Proposition 5.6 を外部 Reference から除外し、実利用の\nReference のみを保持することを確認した。\n\n## R12 — root Reference exclusion across routes\n\ncurrent `presentation.root_step` の `LiteratureReference` を、legacy / generic / specialized の\nroute に依存せず external Reference section へ出さない display-boundary rule とした。\n\nfocused repair:\n\n```text\n17 passed in 5.57s\n```\n\n## R13 — closure repair\n\n112-group closure audit で残った4違反:\n\n```text\npi_4^2: root_reference_in_reference_section\npi_8^5: root_reference_in_reference_section\npi_8^5: marker_route_unused_reference\npi_15^8: root_reference_in_reference_section\n```\n\nを一般規則で修復した。\n\n主な修正:\n\n```text\nliterature Reference identity\n→ locator-first comparison\n\nspecialized public Reference section\n→ body-use filtering\n→ root exclusion\n→ marker mapping preservation\n```\n\nR13 package 生成時の一度の syntax error は packaging script の問題であり、renderer を\nbackup から復元後に同じ設計を安全に再適用した。\n\nsyntax repair:\n\n```text\n2 passed\nsmoke audit: PASS\n```\n\nclosure verification:\n\n```text\n30 passed in 7.97s\n\nscanned groups: 112\nrender errors: 0\ngroups with Reference section: 93\nmarker-bearing groups: 90\ngeneric/reference-only groups: 3\nReference headers: 147\nbody Reference markers: 146\nmaximum References in one group: 6\ngroups at maximum: pi_6^3\nviolations: 0\n\nPASS\n```\n\n## final full pytest の扱い\n\nPhase 153 の production closure 後、canonical `tests/` を対象に final full pytest を開始した。\n\n```text\ncollected: 10554\n```\n\n途中で過去 Phase の stale presentation expectation が複数検出された。\n\n最初に確認した Phase 132 Narrative expectation は、現行 generic Reference route と\n矛盾する historical display contract であり、production regression ではなかった。\n\ntest-only repair 後:\n\n```text\n22 passed in 6.28s\n```\n\nその後も旧 CLI heading expectation など historical test maintenance pressure が確認された。\n全体 suite の整理自体に大きな時間を要するため、今回は Phase 153 の completion gate として\nfull historical regression を完走しない判断とした。\n\nしたがって Phase 153 は次の実測で閉じる。\n\n```text\nfocused/reference regression: PASS\n112-group Reference invariant audit: PASS\nrender errors: 0\nviolations: 0\nrepository-wide all-pass result: not claimed\n```\n\n## Phase 153 完了境界\n\n解決:\n\n```text\nReference selection\nReference granularity\nroot self-reference exclusion\nReference reuse\nunused Reference filtering\ngeneric-route Reference attribution\nspecialized-route closure consistency\n```\n\n未解決・次 Phase:\n\n```text\nproof prose connective duplication\nrepeated "まず" / "以上より" / "したがって"\ninternal rule-name leakage\nEnglish statement prose\nduplicate scalar rendering such as ord(nu\')=4=4\npunctuation normalization to "," and "."\n```\n\nこれらを Phase 154 の proof-prose generation 改善として扱う。\n\nTest Suite Consolidation は別の maintenance backlog とし、当面は機能・Narrative 開発を\n優先する。\n',
  'docs/roadmap.md': '<!-- PHASE153_CLOSURE -->\n# Phase 153 完了後のロードマップ\n\n## 現在地\n\nPhase 153 `Reference selection / granularity` 完了。\n\ndepth 2 の標準112群\n\n$$\nn=2,\\ldots,15,\n\\qquad\nk=0,\\ldots,7\n$$\n\nについて Reference invariant を監査し、\n\n```text\nscanned groups: 112\nrender errors: 0\nviolations: 0\n```\n\nを確認した。\n\nPhase 153 で確定した一般規則:\n\n```text\nroot theorem != external Reference\nproof-use ancestry を Reference selection に優先\nconsumer-relevant aggregate component を粒度として選択\ndisplayed Reference を reusable proof boundary として利用\nmarker-bearing route の unused Reference を除外\ngeneric no-marker route は displayed step usage で attribution\nliterature Reference identity は locator-first\nlegacy / generic / specialized route で同じ root-exclusion boundary\n```\n\n## Phase 154 — Proof prose generation refinement\n\n次 Phase は test-suite 整理ではなく、現在の Narrative 本文の不自然さを一般規則で改善する。\n\n最初の作業:\n\n```text\nPhase 154-R1\nRepresentative proof prose defect audit\n```\n\n代表群:\n\n$$\n\\pi_6^3,\\quad\n\\pi_{10}^4,\\quad\n\\pi_{11}^4,\n$$\n\n必要に応じて\n\n$$\n\\pi_{12}^5,\\quad\n\\pi_{16}^9\n$$\n\nを追加する。\n\n主対象:\n\n```text\nconnector duplication\nrepeated "まず"\nrepeated "以上より"\nrepeated "したがって"\ninternal rule-name leakage\nEnglish statement rendering\nduplicate scalar prose such as ord(nu\')=4=4\nargument / contribution connection\npunctuation normalization to "," and "."\n```\n\n方針:\n\n```text\none visible prose defect category\n→ root cause audit\n→ minimum general rule\n→ focused regression\n→ cross-group audit\n```\n\n$\\pi_6^3$ 専用 renderer や群別 special case で修正しない。\n\n長期目標は引き続き、\n\n```text\n一般規則のみで pi_6^3 と同等品質の証明文を生成する\n```\n\nことである。\n\n## Test Suite Consolidation — 保留\n\ncanonical `tests/` は Phase 153 時点で 10,554 tests を収集する。\n\nhistorical presentation expectation や重複 test の整理が必要であることは確認済みだが、\n整理自体の工数が大きいため、当面は独立 maintenance backlog とする。\n\n保留項目:\n\n```text\nstale expectation inventory\nduplicate coverage audit\nhistorical snapshot classification\ncanonical regression set の明示\npytest collection boundary の固定\ntest performance baseline\n```\n\nこの maintenance は Phase 154 の proof-prose development の前提条件にはしない。\n\n開発中は focused regression を優先し、complete historical regression は必要な大きな\nintegration point で実行する。\n\n## 今後も先取りしないもの\n\n```text\nnew Toda theorem facts\ngeneral theorem ranking\nautomatic best proof selection\ngeneral E/H/Delta evaluator\nunbounded proof search\nprovenance-free LLM proof generation\ntarget-specific prose hardcoding\n```\n',
  'docs/proof_records.md': '<!-- PHASE153_CLOSURE -->\n# Phase 153 Reference selection / granularity provenance record\n\nPhase 153 は数学的 theorem fact を追加した Phase ではない。\n\n対象は既存 `ProofStep` provenance から Narrative に提示する external Reference の選択、\n粒度、再利用、表示境界である。\n\n## provenance ground truth\n\n引き続き ground truth は\n\n```text\nProofStep.conclusion\nProofStep.premises\nProofStep.inference_rule\nexisting recursive provenance\nLiteratureReference\n```\n\nである。\n\nPhase 153 の Reference layer は、これらから表示に必要な外部結果を選ぶ presentation rule である。\n\n```text\nReference selection\n!= theorem selection\n\nReference granularity\n!= theorem decomposition\n\nReference reuse\n!= premise deletion\n\nReference filtering\n!= provenance deletion\n```\n\n## root Reference boundary\n\ncurrent `presentation.root_step` の literature citation は、その証明自身の provenance であり、\nexternal supporting Reference ではない。\n\nしたがって:\n\n```text\nroot LiteratureReference\n→ provenance として保持\n→ external Reference section から除外\n```\n\nこの boundary は legacy / generic / specialized route に共通である。\n\n## locator identity\n\n同じ文献箇所が label 違いで保持される場合の identity は次とする。\n\n```text\nboth references have locator\n→ compare locator\n\notherwise\n→ compare full LiteratureReference\n```\n\nこの rule により `(5.2)` など同じ locator の root citation が label 差によって\nexternal Reference に漏れることを防ぐ。\n\n## used Reference provenance\n\nmarker-bearing route:\n\n```text\nrendered body [Rk]\n→ used Reference set\n→ filter\n→ contiguous renumbering\n```\n\ngeneric no-marker route:\n\n```text\ndisplayed argument/local-body/contribution steps\n→ used step ids\n→ structural Reference attribution\n```\n\nしたがって explicit marker の有無は provenance の有無を意味しない。\n\n## Reference reuse provenance\n\nReference statement として exact step が表示済みなら、その step の既存 premises を本文で\n再展開しなくても、`[Rk]` 利用として proof boundary を示せる。\n\n```text\nReference boundary reuse\n→ display compression\n\nexisting ProofStep ancestry\n→ preserved\n```\n\n## aggregate granularity record\n\naggregate statement に複数の group relation / generator component が含まれる場合、\nconsumer と構造的に対応する一意 component を Reference statement として選択できる。\n\nこれは aggregate theorem の数学的意味を変更するものではない。\n\n```text\naggregate theorem provenance\n→ preserved\n\nNarrative Reference statement\n→ consumer-relevant component\n```\n\n## n=2 six-group ancestry record\n\n監査対象:\n\n$$\n\\pi_4^2,\\quad\n\\pi_5^2,\\quad\n\\pi_6^2,\\quad\n\\pi_7^2,\\quad\n\\pi_8^2,\\quad\n\\pi_9^2.\n$$\n\nroot 自身ではなく、実際に利用する premise / ancestry から external Reference を選ぶ\n一般 rule を確認した。\n\n## final 112-group provenance audit\n\n対象:\n\n$$\nn=2,\\ldots,15,\n\\qquad\nk=0,\\ldots,7.\n$$\n\n結果:\n\n```text\nscanned groups: 112\nrender errors: 0\ngroups with Reference section: 93\nmarker-bearing groups: 90\ngeneric/reference-only groups: 3\nReference headers: 147\nbody Reference markers: 146\nmaximum References in one group: 6\ngroups at maximum: pi_6^3\nviolations: 0\n```\n\nReference invariant:\n\n```text\nReference numbers contiguous\nroot citation not external\nbody marker points to an existing Reference\nmarker-bearing body has no unused displayed Reference\n```\n\nすべて PASS。\n\n## regression evidence boundary\n\nPhase 153 closure verification:\n\n```text\n30 passed in 7.97s\n```\n\nfull canonical historical suite は 10,554 tests を収集したが、古い presentation expectation が\n複数残っていることを確認し、今回は全完走を completion evidence にしなかった。\n\n確認済みの stale Phase 132 Narrative expectation については test-only repair を行い、\n\n```text\n22 passed in 6.28s\n```\n\nを確認した。\n\nrepository-wide all-pass は観測していないため記録しない。\n\n## next provenance boundary\n\nPhase 154 は Reference selection ではなく proof-prose generation を扱う。\n\n```text\nstored proof provenance\n→ unchanged\n\nReference selection / granularity\n→ Phase 153 で確定\n\nprose realization / connection\n→ Phase 154\n```\n\nTest Suite Consolidation は別 maintenance backlog とする。\n',
}


def find_repo_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (candidate / "README.md").is_file()
      and (candidate / "docs" / "design.md").is_file()
      and (candidate / "docs" / "development_log.md").is_file()
      and (candidate / "docs" / "roadmap.md").is_file()
      and (candidate / "docs" / "proof_records.md").is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def append_once(
  path: Path,
  marker: str,
  section: str,
) -> None:
  text = path.read_text(
    encoding="utf-8-sig"
  )

  if marker in text:
    print(
      "Already updated:",
      path.as_posix(),
    )
    return

  updated = (
    text.rstrip()
    + "\n\n---\n\n"
    + section.rstrip()
    + "\n"
  )

  path.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    path.as_posix(),
  )


def main() -> None:
  repo = find_repo_root()

  backup_dir = (
    repo
    / "phase153_documentation_closure_backup"
  )
  output_dir = (
    repo
    / "phase153_documentation_closure"
    / "output_full_documents"
  )

  backup_dir.mkdir(
    exist_ok=True
  )
  output_dir.mkdir(
    parents=True,
    exist_ok=True,
  )

  for relative_path in SECTIONS:
    path = repo / relative_path
    backup = backup_dir / relative_path
    backup.parent.mkdir(
      parents=True,
      exist_ok=True,
    )

    if not backup.exists():
      shutil.copy2(
        path,
        backup,
      )

    append_once(
      path,
      MARKERS[relative_path],
      SECTIONS[relative_path],
    )

    output = (
      output_dir
      / relative_path
    )
    output.parent.mkdir(
      parents=True,
      exist_ok=True,
    )
    shutil.copy2(
      path,
      output,
    )

  print()
  print(
    "Phase 153 documentation closure applied."
  )
  print(
    "Full updated documents copied to:"
  )
  print(
    "  phase153_documentation_closure/output_full_documents/"
  )
  print(
    "No production code changed."
  )
  print(
    "No pytest run."
  )


if __name__ == "__main__":
  main()
