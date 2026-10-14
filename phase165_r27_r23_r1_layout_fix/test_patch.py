from types import SimpleNamespace
import main as cli
import pytest
from phase165_r52_partial_proof import ProofSearchStatus

@pytest.mark.parametrize('status, expected_code',[
    (ProofSearchStatus.COMPLETE,0),
    (ProofSearchStatus.PARTIAL,1),
    (ProofSearchStatus.SEARCH_FAILED,1),
])
def test_r23_group_query_uses_search(monkeypatch,capsys,status,expected_code):
    calls=[]
    def search(*,n,k):
        calls.append((n,k))
        return SimpleNamespace(status=status)
    monkeypatch.setattr(cli,'search_group_structure_automatically',search)
    monkeypatch.setattr(cli,'render_partial_proof_markdown',lambda result:f'{result.status.value}\n')
    assert cli.main(['3','1'])==expected_code
    assert calls==[(3,1)]
    assert status.value in capsys.readouterr().out

@pytest.mark.parametrize('mode',['trace','outline','narrative'])
def test_r23_group_proof_modes_preserved(monkeypatch,capsys,mode):
    calls=[]
    def search(*,n,k):
        calls.append((n,k))
        return SimpleNamespace(status=ProofSearchStatus.PARTIAL)
    monkeypatch.setattr(cli,'search_group_structure_automatically',search)
    monkeypatch.setattr(cli,'render_partial_proof_markdown',lambda result:'partial proof\n')
    assert cli.main(['group-proof','3','1','--mode',mode,'--depth','2'])==1
    assert calls==[(3,1)]
    assert 'partial proof' in capsys.readouterr().out

def test_r23_no_legacy_group_builder_call():
    import ast
    from pathlib import Path
    src=Path(cli.__file__).read_text(encoding='utf-8')
    tree=ast.parse(src)
    calls=[node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)]
    assert 'build_standard_toda_report' not in calls

def test_r23_domain_boundary_preserved(monkeypatch,capsys):
    monkeypatch.setattr(cli,'search_group_structure_automatically',lambda **kw: (_ for _ in ()).throw(AssertionError('should not search')))
    assert cli.main(['2','-2'])==0
    assert 'pi_{0}' in capsys.readouterr().out
