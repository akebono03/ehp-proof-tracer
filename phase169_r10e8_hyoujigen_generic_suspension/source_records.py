"""Reviewed Chapter VI source facts. No mathematical inference is defined here.

HyoujiGen.csv remains the sole source of family ID, stem and minimum n.
These rows only locate fixed source language and its publication order.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChapterVISourceRecord:
    family_id: int
    defining_clause: str
    paragraph_start: str
    paragraph_end: str
    locator: str


CHAPTER_VI_SOURCE_RECORDS = (
    ChapterVISourceRecord(
        family_id=10,
        defining_clause=r"\varepsilon_n:=E^{\,n-3}\varepsilon_3\quad (n\ge3)",
        paragraph_start=r"\paragraph{i). The Elements \(\varepsilon_n\).}",
        paragraph_end=r"\paragraph{ii). The elements \(\,\overline{\nu}_n\).}",
        locator="Chapter VI, i) The Elements epsilon_n (definition)",
    ),
    ChapterVISourceRecord(
        family_id=11,
        defining_clause=r"\overline{\nu}_n:=E^{\,n-6}\overline{\nu}_6\ (n\ge6)",
        paragraph_start=r"\paragraph{ii). The elements \(\,\overline{\nu}_n\).}",
        paragraph_end=r"\paragraph{iii). The elements \(\mu_n\).}",
        locator="Chapter VI, ii) The elements bar-nu_n (definition)",
    ),
    ChapterVISourceRecord(
        family_id=12,
        defining_clause=r"\mu_{n}:=E^{\,n-3}\mu_{3}",
        paragraph_start=r"\paragraph{iii). The elements \(\mu_n\).}",
        paragraph_end=r"\paragraph{iv). The element \(\varepsilon'\).}",
        locator="Chapter VI, iii) The elements mu_n (definition)",
    ),
)
