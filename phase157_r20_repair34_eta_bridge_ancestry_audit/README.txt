Phase157-R20 repair34 runtime audit

Purpose
-------
Determine the exact proof-graph relationship between:

- the eta-family definition premises used to derive eta_6 = E eta_5;
- Proposition 2.2;
- the consumer step H(nu' eta_6) = eta_5^2.

Why
---
repair33 assumed Proposition 2.2 was a visible direct premise of the same
consumer step that carries the eta-family definition premises. The ordering did
not change, so that assumption is false in the current local graph.

This audit prints:
- the target consumer;
- all direct premises;
- breadth-first ancestry with depth and path;
- literature-reference locators;
- current visible body order.

Production code changes: none.
pytest: not run.
