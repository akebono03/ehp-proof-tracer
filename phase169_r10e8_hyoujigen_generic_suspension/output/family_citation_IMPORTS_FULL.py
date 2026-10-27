from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10b_registered_stable_family_binding.family_registry import (
    RegisteredStableFamily,
    read_registered_stable_families,
    registered_family_of,
    registered_stable_family_pair,
)
from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
    CHAPTER_VI_SOURCE_RECORDS,
)
from proof import (
    InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep,
)
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)
