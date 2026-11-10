# Phase 174 R57R1 変更コード・関数全文

## 原因

R57 の `review()` は `git rev-parse HEAD == 0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9` を要求した。その後 R56 のコミットが `develop` に追加されたため、数学的な変更対象の Git blob は一致していても事前監査が拒否した。

## 変更対象の一覧

- 既存：`phase174_r3_r7_r57_narrative_source_cleanup/install.py` の `review()` **全体**。変更位置は既存の `def review(dry_run=False):`。
- 新規：`phase174_r3_r7_r57r1_head_lineage_fix/install.py`。追加位置は ZIP 展開先の新規パッケージ。
- 新規：`phase174_r3_r7_r57r1_head_lineage_fix/run.ps1`。
- 新規：`phase174_r3_r7_r57r1_head_lineage_fix/tests/test_lineage.py`。テスト関数は新規ファイル内。
- **import 変更なし**。R57 の既存の import 節は一切変更しない。

## 修正後の R57 `review()` 関数全文

```python
def review(dry_run=False):
    if git('branch','--show-current') != 'develop':
        raise RuntimeError('develop branch required')
    if Path(git('rev-parse','--show-toplevel')).resolve()!=ROOT.resolve():
        raise RuntimeError('extract R57 directly into the repository root')
    # The reviewed base commit may be followed by R56's own release commit.
    # A descendant is allowed ONLY when every reviewed target blob and each
    # local R56 rule/test source still matches its independently pinned hash.
    lineage = subprocess.run(
        ('git', 'merge-base', '--is-ancestor', HEAD, 'HEAD'),
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if lineage.returncode != 0:
        raise RuntimeError('unreviewed HEAD lineage (R57 reviewed base not an ancestor): '
                           + lineage.stderr.decode('utf-8', 'replace'))
    if git('diff','--cached','--name-only'):
        raise RuntimeError('staged files require separate review')
    states={}
    for name,func in PATCHES.items():
        path=ROOT/name
        if not path.is_file():
            raise RuntimeError('required R56 or baseline file missing: '+name)
        data=path.read_bytes()
        content,bom,eol=normalize(data)
        if name in PINS:
            if git('rev-parse','HEAD:'+name)!=PINS[name]:
                raise RuntimeError('unreviewed committed blob: '+name)
            raw=git('show','HEAD:'+name,binary=True)
            baseline=normalize(raw)[0]
            intended=func(baseline)
            if content not in (baseline,intended):
                raise RuntimeError('unreviewed local edits: '+name)
            revised=intended
        else:
            current_hash=sha256(content.encode('utf-8'))
            if current_hash==LOCAL_SHA256[name]:
                revised=func(content)
            elif current_hash==AFTER_SHA256[name]:
                revised=content
            else:
                raise RuntimeError('R56 local rule/test differs from reviewed input: '+name)
        ast.parse(revised,filename=name)
        future=bom+revised.replace('\n',eol).encode('utf-8')
        states[name]=(data,future,revised)
    return states
```

## 修正後のファイル全文

`R57_INSTALL_FULL_AFTER.py.txt` に R57 の修正後 `install.py` の全文、`R57_INSTALL_ORIGINAL_AUDITED.py.txt` に修正前全文を含む。R57R1 自体の実行コードとテスト関数全文は本 ZIP 内の `install.py`、`run.ps1`、`tests/test_lineage.py` を参照できる。

## 変更前後の SHA-256

- original: `f14d6930e236bdd97b85cc23a77f15fe17bc71cf7c087f1becd132ccf4b9ccf2`
- amended: `6a4df3c77edd7a0abd902d28782d12a63ebb6bd69f8c7d03e8efff601cd1e32e`

## 実行する限定 pytest

```powershell
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase174_r3_r7_r57r1_head_lineage_fix/tests/test_lineage.py
```

その後、既存 R57 の `run.ps1` で既定の4グループの限定 pytest と実公開監査を行う。全体 pytest は Phase 終了時のみ。

## 完了条件と次の境界

1. R57R1 Source Guard PASS。レビュー済み基点コミットの子孫かつ既存のファイル固定値をすべて照合。
2. R57 の DryRun と公開監査が PASS。
3. `pi11^6`、`pi12^7` の根の complete と、Proposition 2.7 の不要な再導入がないことを確認。
4. 新しい GIVEN、数学的規則、専用 Narrative は追加しない。

R57R1 は **Source Guard の訂正のみ**。原文 (5.10) の内部の符号付き型の再設計や引用表示完全統一は、次の監査・Phase の別範囲。
