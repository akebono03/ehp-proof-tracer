# Phase 162 R10-R7 Repair 1

R10-R7 の移送先直接一致条件が、既存の (4.5) の一般形から特殊化した stable 群を誤って除外したため、元の表示契約を復旧する限定修正です。

変更対象: toda_group_proof_narrative_transport_link.py の import と render_suspension_transport_link() 全体。
新規: test_r10_r7_repair1.py（既存の R10-R7 と R4-B テストも再実行）。

今回の判定は完全な一般的特殊化検証ではありません。推論で再構築した最終目標には移送先一致を要求し、既存の非 INFERENCE な特殊化根は位数・既存の移送 witness を保つ場合に従来の表示を維持します。出典・証明木の改変はしません。

完了条件: focused pytest にて既存 stable と π5³ が共存すること。Phase 162 終了時以外には全体 pytest を実行しません。
次の Phase 境界: stable 特殊化の型付き根拠を証明木へ登録して厳密に検証することは今は行いません。
