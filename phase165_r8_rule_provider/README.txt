Phase 165 R8: general inference-rule catalog and inverse pattern provider.
New root file: phase165_r8_rule_provider.py
New test file: tests/test_phase165_r8_rule_provider.py
New audit: phase165_r8_rule_provider/audit.py
Rule discovery is limited to declared inference-rule modules, and only invertible
fully-bound patterns produce backward expansions. No source promotion.
The provider is not yet wired to the public Goal-only entry, and no complete
pi5_3 proof is claimed. No full pytest.
