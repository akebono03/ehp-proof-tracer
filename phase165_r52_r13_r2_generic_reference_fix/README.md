# R52-R13-R2 focused regression repair

Run `run.ps1` from the repository root after the existing R52-R13-R1 installation.

This changes only the registered composite's explicit component metadata, the generic component index's interpretation of that metadata, and the common web adapter's acceptance of a typed GIVEN root. It does not convert legacy INFERENCE statements to GIVEN or implement the next-phase specialization rules.

Targeted pytest only. No full-suite pytest.
