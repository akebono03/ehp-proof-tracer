"""Extract only the rendered Narrative area of a Flask HTML response.

This module parses already-rendered HTML. It does not verify mathematical
proofs, infer source citations, or modify the Web application.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass(frozen=True)
class NarrativeHTML:
    found: bool
    headings: tuple[str, ...]
    visible_text: str
    math_latex: tuple[str, ...]


class _NarrativeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.found = False
        self.inside = False
        self.div_depth = 0
        self.heading_active = False
        self.heading_parts: list[str] = []
        self.headings: list[str] = []
        self.visible_parts: list[str] = []
        self.math_latex: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if not self.inside:
            if tag == "div" and attributes.get("id") == "group-proof-rendered-lines":
                if self.found:
                    raise ValueError("duplicate rendered Narrative containers")
                self.found = True
                self.inside = True
                self.div_depth = 1
            return
        if tag == "div":
            self.div_depth += 1
        if tag == "h4":
            if self.heading_active:
                raise ValueError("nested Narrative headings")
            self.heading_active = True
            self.heading_parts = []
        if attributes.get("data-latex") is not None:
            self.math_latex.append(attributes["data-latex"])

    def handle_endtag(self, tag: str) -> None:
        if not self.inside:
            return
        if tag == "h4" and self.heading_active:
            self.headings.append(" ".join("".join(self.heading_parts).split()))
            self.heading_active = False
            self.heading_parts = []
        if tag == "div":
            self.div_depth -= 1
            if self.div_depth < 0:
                raise ValueError("unbalanced Narrative HTML div")
            if self.div_depth == 0:
                self.inside = False

    def handle_data(self, data: str) -> None:
        if self.inside:
            self.visible_parts.append(data)
            if self.heading_active:
                self.heading_parts.append(data)


def parse_narrative_html(document: str) -> NarrativeHTML:
    """Read headings, text, and MathJax inputs from the rendered proof section."""
    if not isinstance(document, str):
        raise TypeError("HTML document must be a string")
    parser = _NarrativeParser()
    parser.feed(document)
    parser.close()
    if parser.inside or parser.div_depth != 0 or parser.heading_active:
        raise ValueError("incomplete Narrative HTML container")
    return NarrativeHTML(
        found=parser.found,
        headings=tuple(parser.headings),
        visible_text=" ".join(" ".join(parser.visible_parts).split()),
        math_latex=tuple(parser.math_latex),
    )
