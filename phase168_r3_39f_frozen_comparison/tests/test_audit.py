"""Focused, pure tests for benchmark explanation checks."""
from phase168_r3_39f_frozen_comparison.audit import assess, compact


def test_pi32_flags_missing_justifications():
    proof = (r"$H: \pi_{3}^{2}\to\pi_{3}^{3}$ は単射." + "\n"
             + r"完全性と懸垂写像の同型性より, $\Delta$ は零写像." + "\n")
    checks = {item["key"]: item["present"] for item in assess("pi3_2", proof)}
    assert checks["exactness_for_injectivity"] is False
    assert checks["delta_image_kernel_zero"] is False
    assert checks["hopf_iso_from_bijectivity"] is False


def test_pi54_flags_missing_specialization_and_wrong_order():
    proof = (r"$E(\eta_{3})=\eta_{4}$." + "\n"
             + r"$\pi_{4}^{3}=\mathbb{Z}/2\{\eta_{3}\}$." + "\n"
             + r"$E:\pi_{4}^{3}\to\pi_{5}^{4}$ は同型.")
    checks = {item["key"]: item["present"] for item in assess("pi5_4", proof)}
    assert checks["toda45_explicit_substitution"] is False
    assert checks["source_before_generator_image"] is False
    assert checks["specific_map_isomorphism"] is True
    assert compact(" $E : \\pi$ ") == r"E:\pi"
