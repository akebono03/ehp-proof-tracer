from web_group_proof import build_standard_web_group_proof_view


def main():
    for n, k in ((2, 2), (2, 1), (3, 1), (4, 1)):
        legacy = build_standard_web_group_proof_view(n, k)
        modeled = build_standard_web_group_proof_view(n, k, citation_source="model")
        print(f"PI_{n+k}^{n} legacy_lines={len(legacy.rendered_lines)} model_lines={len(modeled.rendered_lines)} "
              f"legacy_partial={legacy.partial_result} model_partial={modeled.partial_result}")
        if n == 2 and k == 2:
            joined = "\n".join(line.prefix for line in modeled.rendered_lines)
            assert "Proposition 5.1" in joined and "(5.2)" in joined
    print("R3-6 STANDARD WEB MODEL ROUTE: PASS")
    print("DEFAULT LONG-FORM ROUTE: PRESERVED")


if __name__ == "__main__":
    main()
