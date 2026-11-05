"""E6: closure check by recording file opens (audit hook) for a toy analysis."""
import sys, os, tempfile, json, io, contextlib
d = tempfile.mkdtemp(prefix="e6_")
open(os.path.join(d, "data.csv"), "w").write("x\n1\n2\n3\n")
open(os.path.join(d, "scale.cfg"), "w").write("10\n")          # undeclared read
analysis = f'''
import os
rows = [int(l) for l in open(r"{d}/data.csv").read().split()[1:]]
scale = int(open(r"{d}/scale.cfg").read())
print(sum(rows) * scale)
'''
declared = {os.path.join(d, "data.csv")}
def run_capture():
    reads = set()
    def hook(ev, args):
        if ev == "open":
            p = args[0]
            if isinstance(p, str) and p.startswith(d): reads.add(p)
    sys.addaudithook(hook)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(analysis, "analysis", "exec"), {})
    return reads, buf.getvalue().strip()
reads, out1 = run_capture()
print("reads:", sorted(os.path.basename(p) for p in reads)); print("declared:", sorted(os.path.basename(p) for p in declared))
print("undeclared_reads:", sorted(os.path.basename(p) for p in reads - declared)); print("closed:", reads <= declared)
open(os.path.join(d, "scale.cfg"), "w").write("20\n")
_, out2 = run_capture()
print("output_before:", out1, "output_after_changing_undeclared_file:", out2, "differs:", out1 != out2)
