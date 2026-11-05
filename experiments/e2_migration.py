"""E2: migration of Git data preserves objects/refs; platform records are not carried by a clone."""
import subprocess, tempfile, os, json, hashlib
def g(args, cwd):
    e = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@x")
    return subprocess.run(["git"] + args, cwd=cwd, env=e, capture_output=True, text=True, check=True).stdout.strip()
d = tempfile.mkdtemp(prefix="e2_"); r = os.path.join(d, "src"); os.makedirs(r)
g(["init", "-q", "-b", "main"], r)
for i in range(20):
    open(os.path.join(r, f"a{i%4}.txt"), "a").write(f"line {i}\n"); g(["add", "-A"], r); g(["commit", "-q", "-m", f"c{i}"], r)
g(["tag", "-a", "v1", "-m", "release"], r); g(["branch", "dev"], r)
# simulated platform record store (what a host keeps outside git)
platform = {"issues": [{"id": 1, "refs": [g(['rev-parse','HEAD'], r)], "text": "PLATFORM_ISSUE_MARKER"}], "reviews": 3, "perms": {"alice": "write"}}
open(os.path.join(d, "platform.json"), "w").write(json.dumps(platform))
m = os.path.join(d, "mirror.git"); g(["clone", "-q", "--mirror", r, m], d)
def objs(path): return set(g(["rev-list", "--all", "--objects"], path).split("\n"))
def refs(path): return g(["for-each-ref", "--format=%(refname) %(objectname)"], path).split("\n")
print("objects_equal:", objs(r) == objs(m))
print("refs_equal:", sorted(refs(r)) == sorted(refs(m)))
print("fsck_clean:", subprocess.run(["git", "fsck", "--strict"], cwd=m, capture_output=True).returncode == 0)
# does the mirror contain anything resembling the platform records?
found = subprocess.run("grep -rl 'PLATFORM_ISSUE_MARKER' . || true", shell=True, cwd=m, capture_output=True, text=True).stdout.strip()
print("platform_records_in_mirror:", bool(found))
print("platform_records_only_in_side_store:", os.path.exists(os.path.join(d, "platform.json")))
