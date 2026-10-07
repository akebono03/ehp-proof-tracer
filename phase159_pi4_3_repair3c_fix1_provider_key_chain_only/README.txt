Phase 159 - repair3c fix1
Provider-key chain-only optimization

原因
----
repair3c performance audit で、_necessity_for_chain() 単体は高速だった。

例:
- pi_12^5 argument 0: chain=1672, necessity_seconds=0.208
- pi_12^5 argument 1: chain=1672, necessity_seconds=0.265

一方 visibility 構築中に KeyboardInterrupt となり、traceback は

  _build_visibility_occurrences()
    -> _provider_keys_for_step()
      -> _necessity_for_chain()
        -> _can_reach_conclusion()

を示した。

_provider_keys_for_step() が必要なのは provider ごとの chain membership だけであり、
necessity 計算そのものは不要。

変更対象
--------
toda_group_proof_narrative_contribution_ordering.py

変更関数
--------
_provider_keys_for_step()

変更内容
--------
旧:
  provider ごとに _necessity_for_chain() を呼び、
  その返値の chain_ids だけを利用。

新:
  provider ごとに _anchored_chain_step_ids() を直接呼び、
  chain_ids だけを利用。

意味上の変更
------------
なし。

- provider key 判定条件は引き続き `step_id in chain_ids`
- chain construction は repair3c のまま
- necessity semantics は repair3c のまま
- pi_4^3 hard-code なし
- argument ownership 変更なし
- renderer 変更なし

新規テスト
----------
tests/test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py

確認内容:
- _provider_keys_for_step() が _anchored_chain_step_ids() を使う
- _provider_keys_for_step() が _necessity_for_chain() を再実行しない
- provider key 判定が `step_id in chain_ids` のまま

Focused pytest
--------------
1. test_phase159_pi4_3_repair3c_fix1_provider_key_chain_only.py
2. test_phase159_pi4_3_repair3c_provider_ancestry_contributions.py
3. test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py
4. test_phase149_rc3_3_minimal_ordering.py

Repository-wide pytest
----------------------
実行しない。Phase 159 の最後にのみ実行する。

完了条件
--------
- fix1 structural regression PASS
- pi_4^3 repair3c regression PASS
- phase144 contribution production regression が停止せず完走
- phase149 ordering regression PASS
- repository-wide pytest は未実行のまま

次との境界
----------
この fix1 は performance regression の除去だけ。
public pi_4^3 Narrative の prose 順序・重複・Reference linkage は変更しない。
focused regression 完走後に public Narrative を再監査する。
