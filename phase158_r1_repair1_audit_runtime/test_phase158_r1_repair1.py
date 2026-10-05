from audit_phase158_r1_repair1 import (
    _inspect_rendered,
)


def test_phase158_r1_repair1_inspection_accepts_full_contract():
    rendered = "\n".join(
        (
            "# Group proof narrative",
            "",
            "## 証明対象",
            "",
            "TARGET",
            "",
            "## 使用する結果",
            "",
            "[R1] RESULT",
            "",
            "---",
            "",
            "## 証明",
            "",
            "PROOF",
            "",
            "□",
            "",
        )
    )

    inspection = _inspect_rendered(
        rendered
    )

    assert inspection["has_title"] is True
    assert inspection["has_target"] is True
    assert inspection["has_reference"] is True
    assert inspection["has_proof"] is True
    assert inspection["ends_with_qed"] is True
    assert inspection["full_contract"] is True


def test_phase158_r1_repair1_inspection_detects_missing_target():
    rendered = "\n".join(
        (
            "# Group proof narrative",
            "",
            "## 使用する結果",
            "",
            "[R1] RESULT",
            "",
            "## 証明",
            "",
            "PROOF",
            "",
            "□",
            "",
        )
    )

    inspection = _inspect_rendered(
        rendered
    )

    assert inspection["has_target"] is False
    assert inspection["full_contract"] is False
    assert "target" in str(
        inspection["missing_sections"]
    )


def test_phase158_r1_repair1_repo_root_is_importable():
    from toda_calculation_facade import (
        build_standard_toda_report,
    )

    report = build_standard_toda_report(
        n=3,
        k=3,
    )

    assert report.candidates
