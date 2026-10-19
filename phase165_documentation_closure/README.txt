Phase 165 document closure
Run from project root:
Expand-Archive -Path "$HOME\Downloads\phase165_documentation_closure.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_documentation_closure\run.ps1"

Targets:
README.md (English)
docs/design.md (Japanese)
docs/development_log.md (Japanese, append)
docs/roadmap.md (Japanese)
docs/proof_records.md (Japanese, append)

The tool reads the CURRENT FULL local documents, backs up complete originals,
writes updated complete files to phase165_documentation_closure_results/<UTC>/updated_full_documents,
and replaces the five live documents. No pytest is run.
It stops without changes when a file is missing or closure was already applied.
