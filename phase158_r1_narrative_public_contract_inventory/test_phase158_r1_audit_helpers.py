from audit_phase158_r1 import (
    _inspect_rendered,
)


def test_phase158_r1_inspection_accepts_full_contract():
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


def test_phase158_r1_inspection_detects_current_generic_missing_target():
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
    assert inspection["has_reference"] is True
    assert inspection["has_proof"] is True
    assert inspection["ends_with_qed"] is True
    assert inspection["full_contract"] is False
    assert "target" in str(
        inspection["missing_sections"]
    )


def test_phase158_r1_inspection_requires_qed_at_end():
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
            "## 証明",
            "",
            "PROOF",
            "",
        )
    )

    inspection = _inspect_rendered(
        rendered
    )

    assert inspection["ends_with_qed"] is False
    assert inspection["full_contract"] is False
