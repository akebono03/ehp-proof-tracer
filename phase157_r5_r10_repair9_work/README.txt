Phase157 R5-R10 repair9

repair8 result:
- 67 passed
- 5 failed

All 5 failures came from historical public-Reference expectations:
- Phase156 frontier tests correctly show that Lemma 5.4 and (5.2) are on the
  internal reference frontier.
- Phase157 relevance selection subsequently prunes them from the public
  Reference section.
- The current public headers are:
  (5.3), Proposition 5.3, Proposition 5.6.

repair9:
- Production code changes: none.
- Keep the internal frontier assertions unchanged.
- Update only public-output expectations to the Phase157 relevance contract.

Full repository pytest remains deferred until Phase157 closure.
