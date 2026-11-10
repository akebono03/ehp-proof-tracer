"""R55: pin the GitHub-reviewed mathematical and common-Renderer sources."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = 'phase168_r3_5_model_renderer.py'
REVIEWED_HEAD = '40db3a00ca8be58e589e0949e6a70dcedd3b9cf5'
BLOBS = {
    TARGET: '64e0570e8462ee0361ed07afab836c66ce8e7895',
    'phase168_r3_26_exactness_projection.py': 'a62fef3bce2150510e1c487ac6c381227b9a0860',
    'web_group_proof.py': '2c66da9c8e80a13812a63b6adda34c9414d8413c',
    'web_app.py': '6f95663df5cbf028bb16d1f05dca62db2e3fc00e',
    'templates/index.html': '7af2afa40b92b8c1ec3916cf9759516c158b989f',
    'phase165_r55_nk_only_goal.py': 'e436879f578148fe5c30f5a34974bea3425108b2',
    'phase165_r52_r3_web_adapter.py': 'dda215780c0468cf421592aff86c79b1f5482eed',
    'phase174_r3_r7_r54_public_http_narrative_audit/audit.py': '505192a0e166672908322a8e6a2de4f59f23a6ab',
    'phase174_r3_r7_r54_public_http_narrative_audit/tests/test_http.py': 'f7c72f95d055a9d9fd7f7f13529b740a6c431334',
}


def git(*args: str) -> bytes:
    proc = subprocess.run(('git',) + args,cwd=ROOT,capture_output=True,check=True)
    return proc.stdout


def sha_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Verify HEAD, index, all reviewed blobs, and the exact renderer patch."""
    from phase174_r3_r7_r55_common_exactness_intro.patch import replace_lines_preserving_eol
    if Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()!=ROOT.resolve():
        raise RuntimeError('R55 directory must be unpacked under repo root')
    if git('branch','--show-current').decode().strip()!='develop':
        raise RuntimeError('R55 expects develop')
    head=git('rev-parse','HEAD').decode().strip()
    remote=git('ls-remote','origin','refs/heads/develop').decode().strip().split()
    if head!=REVIEWED_HEAD or not remote or remote[0]!=REVIEWED_HEAD:
        raise RuntimeError('R55 requires the reviewed live GitHub develop HEAD')
    if git('diff','--cached','--name-only').strip():
        raise RuntimeError('Staged files require separate review')
    changed=tuple(git('diff','--name-only').decode().splitlines())
    if changed not in ((),(TARGET,)):
        raise RuntimeError('R55 found unrelated tracked edits: '+repr(changed))
    for file,blob in BLOBS.items():
        baseline=git('show','HEAD:'+file)
        if sha_blob(baseline)!=blob:
            raise RuntimeError('Reviewed GitHub mathematical or renderer source changed: '+file)
        actual=(ROOT/file).read_bytes()
        if file != TARGET and actual.replace(b'\r\n',b'\n')!=baseline.replace(b'\r\n',b'\n'):
            raise RuntimeError('Tracked source differs from GitHub HEAD: '+file)
    previous=git('show','HEAD:'+TARGET)
    actual=(ROOT/TARGET).read_bytes()
    def norm(blob:bytes)->str:
        return blob.decode('utf-8-sig').replace('\r\n','\n')
    desired=replace_lines_preserving_eol(norm(previous))
    installed=(norm(actual)==desired)
    if changed==() and norm(actual)!=norm(previous):
        raise RuntimeError('Renderer changed without Git status evidence')
    if changed==(TARGET,) and not installed:
        raise RuntimeError('Unreviewed renderer edit or mixed patch')
    return {
        'source_guard':'PASS', 'local_head':head,'remote_head':remote[0],
        'reviewed_blobs':len(BLOBS),'tracked_changes':changed,
        'r55_renderer_installed':installed,
        'new_given':0,'new_mathematical_rules':0,'full_pytest':False,
    }
