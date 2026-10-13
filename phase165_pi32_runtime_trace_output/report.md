# Phase 165 pi3^2 Renderer Runtime Trace

## 結果

- 状態: `ok`
- 取得したイベント: 32
- 本番コード変更: なし
- pytest: 未実施

## ステージ別記録

### 1. narrative.phase164_contract — NOT_FOUND

```json
{
  "stage": "narrative.phase164_contract",
  "status": "NOT_FOUND"
}
```

### 2. web.presentation — ok

```json
{
  "type": "TodaGroupProofPresentation",
  "nodes": 15,
  "edges": 14,
  "selected_steps": [
    {
      "step_id": 2696681189056,
      "type": "MapIsomorphism",
      "conclusion": "MapIsomorphism(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))",
      "rule": "INFERENCE",
      "inference_rule": "generic injective and surjective imply isomorphism",
      "premise_ids": [
        2696681179264,
        2696681188192
      ],
      "premise_types": [
        "MapInjective",
        "MapSurjective"
      ]
    },
    {
      "step_id": 2696681179264,
      "type": "MapInjective",
      "conclusion": "MapInjective(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))",
      "rule": "INFERENCE",
      "inference_rule": "EHP: preceding zero group and exactness imply Hopf injectivity",
      "premise_ids": [
        2696681192320,
        2696681189584
      ],
      "premise_types": [
        "TodaPrimaryGroupZeroStatement",
        "TodaProp42ExactnessStatement"
      ]
    },
    {
      "step_id": 2696681188192,
      "type": "MapSurjective",
      "conclusion": "MapSurjective(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))",
      "rule": "INFERENCE",
      "inference_rule": "EHP: subsequent zero delta and exactness imply Hopf surjectivity",
      "premise_ids": [
        2696681186368,
        2696681182384
      ],
      "premise_types": [
        "TodaDeltaZeroStatement",
        "TodaProp42ExactnessStatement"
      ]
    },
    {
      "step_id": 2696681186368,
      "type": "TodaDeltaZeroStatement",
      "conclusion": "TodaDeltaZeroStatement(map=TodaDeltaMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1)))",
      "rule": "INFERENCE",
      "inference_rule": "EHP: suspension isomorphism plus Delta-E exactness implies Delta zero",
      "premise_ids": [
        2696681185072,
        2696681184256
      ],
      "premise_types": [
        "TodaSuspensionIsomorphismStatement",
        "TodaProp42ExactnessStatement"
      ]
    },
    {
      "step_id": 2696681185072,
      "type": "TodaSuspensionIsomorphismStatement",
      "conclusion": "TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1), target_group=TodaPrimaryGroup(group_dimension=2, sphere_dimension=2)))",
      "rule": "INFERENCE",
      "inference_rule": "diagonal free cyclic suspension on generators implies isomorphism",
      "premise_ids": [
        2696681180992,
        2696681180800,
        2696680712624
      ],
      "premise_types": [
        "Relation",
        "Relation",
        "GeneratorSuspension"
      ]
    }
  ]
}
```

### 3. web.narrative — ok

```json
{
  "type": "str",
  "length": 728,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```

### 4. narrative.stable_shortcut — ok

```json
{
  "type": "NoneType",
  "repr": "None"
}
```

### 5. narrative.baseline — ok

```json
{
  "type": "str",
  "length": 717,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 6. narrative.contributions — ok

```json
{
  "type": "str",
  "length": 705,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 7. contrib.base_argument_markdown — ok

```json
{
  "type": "str",
  "length": 331,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$"
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 0,
    "これより": 0,
    "単射": 0,
    "全射": 0,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{3}^{3} = \\mathbb{Z}\\{\\iota_{3}\\}$\n\n$H(\\eta_{2}) = \\iota_{3}$.\n\n以上より, \n\n$\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}$"
}
```

### 8. contrib.insert_contributions — ok

```json
{
  "type": "str",
  "length": 640,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 0,
    "これより": 4,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\nこれより, \n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, \n\n$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\nこ"
}
```

### 9. contrib.references_initial — ok

```json
{
  "type": "tuple",
  "count": 3,
  "items": [
    {
      "type": "TodaGroupProofNarrativeReferenceEntry",
      "number": 1,
      "locator": "(5.1)",
      "steps": 4
    },
    {
      "type": "TodaGroupProofNarrativeReferenceEntry",
      "number": 2,
      "locator": "Proposition 5.1",
      "steps": 1
    },
    {
      "type": "TodaGroupProofNarrativeReferenceEntry",
      "number": 3,
      "locator": "Proposition 4.2",
      "steps": 3
    }
  ]
}
```

### 10. contrib.references_fixed_boundary — ok

```json
{
  "type": "tuple",
  "count": 0,
  "items": []
}
```

### 11. contrib.references_statement_selection — ok

```json
{
  "type": "tuple",
  "count": 2,
  "items": [
    {
      "type": "tuple",
      "count": 0,
      "items": []
    },
    {
      "type": "dict",
      "count": 0,
      "keys": []
    }
  ]
}
```

### 12. contrib.references_exclude_root — ok

```json
{
  "type": "tuple",
  "count": 2,
  "items": [
    {
      "type": "tuple",
      "count": 0,
      "items": []
    },
    {
      "type": "dict",
      "count": 0,
      "keys": []
    }
  ]
}
```

### 13. contrib.build_reason_sidecar — ok

```json
{
  "type": "TodaGroupProofNarrativeReasonSidecar",
  "count": 2,
  "kinds": {
    "EXACTNESS_TO_MAP_PROPERTY": 2
  },
  "selected": [
    {
      "kind": "EXACTNESS_TO_MAP_PROPERTY",
      "conclusion": {
        "step_id": 2696681179264,
        "type": "MapInjective",
        "conclusion": "MapInjective(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))",
        "rule": "INFERENCE",
        "inference_rule": "EHP: preceding zero group and exactness imply Hopf injectivity",
        "premise_ids": [
          2696681192320,
          2696681189584
        ],
        "premise_types": [
          "TodaPrimaryGroupZeroStatement",
          "TodaProp42ExactnessStatement"
        ]
      },
      "premises": [
        {
          "step_id": 2696681192320,
          "type": "TodaPrimaryGroupZeroStatement",
          "conclusion": "TodaPrimaryGroupZeroStatement(group=TodaPrimaryGroup(group_dimension=2, sphere_dimension=1))",
          "rule": "GIVEN",
          "inference_rule": "Toda (5.1)",
          "premise_ids": [],
          "premise_types": []
        },
        {
          "step_id": 2696681189584,
          "type": "TodaProp42ExactnessStatement",
          "conclusion": "TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(source_term=TodaPrimaryGroup(group_dimension=2, sphere_dimension=1), middle_term=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_term=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3), first_map=MapSymbol(name='E'), second_map=MapSymbol(name='H')))",
          "rule": "GIVEN",
          "inference_rule": "Toda Proposition 4.2",
          "premise_ids": [],
          "premise_types": []
        }
      ]
    },
    {
      "kind": "EXACTNESS_TO_MAP_PROPERTY",
      "conclusion": {
        "step_id": 2696681188192,
        "type": "MapSurjective",
        "conclusion": "MapSurjective(map=TodaHopfInvariantMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3)))",
        "rule": "INFERENCE",
        "inference_rule": "EHP: subsequent zero delta and exactness imply Hopf surjectivity",
        "premise_ids": [
          2696681186368,
          2696681182384
        ],
        "premise_types": [
          "TodaDeltaZeroStatement",
          "TodaProp42ExactnessStatement"
        ]
      },
      "premises": [
        {
          "step_id": 2696681186368,
          "type": "TodaDeltaZeroStatement",
          "conclusion": "TodaDeltaZeroStatement(map=TodaDeltaMap(source_group=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1)))",
          "rule": "INFERENCE",
          "inference_rule": "EHP: suspension isomorphism plus Delta-E exactness implies Delta zero",
          "premise_ids": [
            2696681185072,
            2696681184256
          ],
          "premise_types": [
            "TodaSuspensionIsomorphismStatement",
            "TodaProp42ExactnessStatement"
          ]
        },
        {
          "step_id": 2696681182384,
          "type": "TodaProp42ExactnessStatement",
          "conclusion": "TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(source_term=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), middle_term=TodaPrimaryGroup(group_dimension=3, sphere_dimension=3), target_term=TodaPrimaryGroup(group_dimension=1, sphere_dimension=1), first_map=MapSymbol(name='H'), second_map=MapSymbol(name='Δ')))",
          "rule": "GIVEN",
          "inference_rule": "Toda Proposition 4.2",
          "premise_ids": [],
          "premise_types": []
        }
      ]
    }
  ]
}
```

### 14. contrib.insert_reasons — ok

```json
{
  "type": "str",
  "length": 716,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, \n\n$E: \\pi"
}
```

### 15. contrib.suppress_reference_internal — ok

```json
{
  "type": "str",
  "length": 716,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, \n\n$E: \\pi"
}
```

### 16. contrib.suppress_reference_duplicates — ok

```json
{
  "type": "str",
  "length": 716,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, \n\n$E: \\pi"
}
```

### 17. contrib.link_body_consumers — ok

```json
{
  "type": "str",
  "length": 716,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, \n\n$E: \\pi"
}
```

### 18. contrib.normalize_connectors — ok

```json
{
  "type": "str",
  "length": 710,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{"
}
```

### 19. contrib.merge_exactness — ok

```json
{
  "type": "str",
  "length": 837,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である.",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{"
}
```

### 20. contrib.normalize_connectors — ok

```json
{
  "type": "str",
  "length": 837,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である.",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{"
}
```

### 21. contrib.dangling_connectors — ok

```json
{
  "type": "str",
  "length": 837,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である.",
    "$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 2,
    "全射": 2,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である.\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射である.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{"
}
```

### 22. contrib.order_reason — ok

```json
{
  "type": "str",
  "length": 705,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 23. contrib.order_reason — ok

```json
{
  "type": "str",
  "length": 705,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 24. contrib.order_reason — ok

```json
{
  "type": "str",
  "length": 705,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 25. contrib.link_body_consumers — ok

```json
{
  "type": "str",
  "length": 705,
  "delta_zero": [
    "$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像である."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": "$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n$\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}$\n\n$\\pi_{2}^{1} = 0$\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_{2}\\}$\n\nこれより, $E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型写像である.\n\n$\\pi_{3}^{3} \\xrightarrow{Δ} \\pi_{1}^{1} \\xrightarr"
}
```

### 26. contrib.reference_section — ok

```json
{
  "type": "str",
  "length": 0,
  "delta_zero": [],
  "hopf_iso": [],
  "reason_markers": {
    "完全性より": 0,
    "これより": 0,
    "単射": 0,
    "全射": 0,
    "使用する結果": 0,
    "[R": 0
  },
  "reference_section_excerpt": null,
  "excerpt": ""
}
```

### 27. contrib.references_statement_selection — ok

```json
{
  "type": "tuple",
  "count": 2,
  "items": [
    {
      "type": "tuple",
      "count": 0,
      "items": []
    },
    {
      "type": "dict",
      "count": 0,
      "keys": []
    }
  ]
}
```

### 28. narrative.phase158_contract — ok

```json
{
  "type": "str",
  "length": 739,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型写像である."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```

### 29. narrative.phase159_map_property — ok

```json
{
  "type": "str",
  "length": 729,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```

### 30. narrative.phase159_numbered_reason — ok

```json
{
  "type": "str",
  "length": 729,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```

### 31. narrative.phase159_reorder — ok

```json
{
  "type": "str",
  "length": 729,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```

### 32. narrative.final_connector_cleanup — ok

```json
{
  "type": "str",
  "length": 728,
  "delta_zero": [
    "\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.",
    "これより, $\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ は零写像."
  ],
  "hopf_iso": [
    "$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."
  ],
  "reason_markers": {
    "完全性より": 2,
    "これより": 2,
    "単射": 1,
    "全射": 1,
    "使用する結果": 1,
    "[R": 0
  },
  "reference_section_excerpt": "\n\n---\n\n",
  "excerpt": "# Group proof narrative\n\n## 証明対象\n\n\\[\n\\pi_{3}^{2} = \\mathbb{Z}\\{\\eta_{2}\\}.\n\\]\n\n## 使用する結果\n\n---\n\n## 証明\n\n$\\pi_{3}^{2}$ の群構造を決定するために, 次の完全列を考える.\n\n\\[\n\\pi_{2}^{1} \\xrightarrow{E} \\pi_{3}^{2} \\xrightarrow{H} \\pi_{3}^{3} \\xrightarrow{\\Delta} \\pi_{1}^{1} \\xrightarrow{E} \\pi_{2}^{2}.\n\\]\n\n$\\pi_{2}^{1} = 0$.\n\n完全性より, $H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は単射.\n\n$\\pi_{1}^{1} = \\mathbb{Z}\\{\\iota_{1}\\}$.\n\n$\\pi_{2}^{2} = \\mathbb{Z}\\{\\iota_"
}
```
