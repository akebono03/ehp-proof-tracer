# Phase 150 / RC4-5D-1

Audit only. No production or existing-test changes.

Purpose:

- locate the recursive `ord(nu-prime)=4` proof step;
- print its direct typed premises;
- inspect nested premise types;
- report which direct premises survive in the depth-2 presentation;
- reject the unsafe assumption that a double relation and an order-two
  right-hand side alone imply order four.

This package does not implement a new Narrative reason kind.

Repository-wide tests are intentionally deferred until the end of Phase 150.
