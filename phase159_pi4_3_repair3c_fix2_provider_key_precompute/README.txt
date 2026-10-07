Phase 159 - repair3c fix2
Provider-key precompute optimization

原因
----
fix1 後も phase144_6_r5_42 の fixture setup が 108 秒以上かかり、
KeyboardInterrupt となった。

traceback:
  build_toda_group_proof_narrative_ordered_contributions
    -> _build_visibility_occurrences
      -> _provider_keys_for_step
        -> _anchored_chain_step_ids
          -> _reverse_distances

fix1 では necessity の再計算は除去したが、
provider key を求める hidden step ごとに、provider ごとの
_anchored_chain_step_ids() を再実行していた。

変更対象
--------
toda_group_proof_narrative_contribution_ordering.py

変更内容
--------
1. 新規 helper:
   _provider_keys_by_step_id()

   argument ごとに一度、
   各 supporting-block provider の chain_ids を構築し、
   step_id -> provider_keys の辞書を作る。

2. _build_visibility_occurrences()

   hidden step loop の前に上記辞書を一度作り、
   occurrence ごとの provider key は辞書参照だけにする。

3. _provider_keys_for_step()

   既存 API / 既存 inspection test の契約維持のため変更しない。

意味上の変更
------------
なし。

- provider key は従来どおり provider 単独 chain の membership で決定
- repair3c upstream ancestry semantics は変更しない
- necessity semantics は変更しない
- pi_4^3 hard-code なし
- argument ownership 変更なし
- renderer 変更なし

新規テスト
----------
tests/test_phase159_pi4_3_repair3c_fix2_provider_key_precompute.py

Focused pytest
--------------
- repair3c fix1 structural regression
- repair3c fix2 structural regression
- pi_4^3 repair3c focused regression
- phase144_6_r5_42 contribution production regression
- phase149_rc3_3 minimal ordering regression

Repository-wide pytest
----------------------
実行しない。Phase 159 の最後にのみ実行する。

完了条件
--------
- provider chain construction が occurrence ごとではなく provider ごとに一回になる
- pi_4^3 repair3c の4事実が維持される
- phase144_6_r5_42 が停止せず完走する
- phase149_rc3_3 が PASS
- full pytest は未実行

次との境界
----------
fix2 は performance regression の解消のみ。
public pi_4^3 Narrative の内容修正は行わない。
focused regression 完走後に public Narrative を再監査する。
