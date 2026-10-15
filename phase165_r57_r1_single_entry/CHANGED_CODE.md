# 変更対象：`web_group_proof.py`

変更関数：`build_standard_web_group_proof_view`。import 変更なし。クラス変更なし。新規関数は新規ファイルの `install.py` と `audit_routes.py` に全文収録。

```python
def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:
  """Use the registered n,k goal and shared proof Web adapter for every group."""
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for positive-dimensional group queries")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  from phase165_r55_nk_only_goal import search_group_from_registered_goal
  from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view

  result = search_group_from_registered_goal(n=n, k=k)
  return build_partial_web_group_proof_view(
    result,
    max_depth=max_depth,
    mode=mode,
  )
```

新規テスト関数3件、必要 import の全文：`test_phase165_r57_r1_single_entry.py` に収録。
