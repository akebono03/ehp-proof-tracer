# Phase 165 R6-1: 同名モジュール修正

対象: `phase165_r52_r7_registered_common_proof/phase165_r52_r7_registered_common_proof.py` 全体。ルート同名モジュールは変更しない。

Python の import が参照する package 側へ、撤去済みのルート版を安全確認後に同期する。変更前をバックアップする。文献 Registry、共通探索、他の API は変更しない。

`run.ps1` で同期後、対象 pytest を実行する。全体 pytest は実施しない。次の R6-2 の一般逆向き規則実装は今回行わない。
