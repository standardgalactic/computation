import csv, re, difflib, json
inv=[r for r in csv.DictReader(open("complete_learning_inventory_revised.csv",encoding="utf-8-sig")) if r["source"].startswith("Handwritten")]
tx=list(csv.DictReader(open("notebook_transcription_2016_2017.csv",encoding="utf-8-sig")))
b1=[t for t in tx if int(t["sequence_in_batch"])<=81]; b2=[t for t in tx if int(t["sequence_in_batch"])>81]
def nd(s): return re.sub(r"\s+"," ",s.lower().strip().replace("april","apr").replace("june","jun").replace("july","jul"))
def nt(s):
    s=re.sub(r"\(.*?\)","",s.lower()); s=re.sub(r"^the ","",s.strip()); return re.sub(r"[^a-z0-9]+"," ",s).strip()
def sim(a,b):
    a,b=nt(a),nt(b); r=difflib.SequenceMatcher(None,a,b).ratio()
    return max(r, 0.9 if (a in b or b in a) and min(len(a),len(b))>=5 else 0)
used={}; 
for pas in (1,2):
    for t in b2:
        if t["entry_id"] in used: continue
        best=None
        for i,r in enumerate(inv):
            if i in used.values(): continue
            s=sim(t["title"],r["title"]); sd=t["date_text"] and nd(t["date_text"])==nd(r["date_text"])
            ok = (sd and s>=0.4) if pas==1 else (s>=0.8)
            if ok and (best is None or s>best[0]): best=(s,i)
        if best: used[t["entry_id"]]=best[1]
un=[t for t in b2 if t["entry_id"] not in used]
print("batch2 matched",len(used),"unmatched",len(un))
for t in un: print("TX-UNMATCHED",t["entry_id"],t["title"],"|",t["date_text"])
for i,r in enumerate(inv):
    if i not in used.values(): print("INV-UNUSED",r["entry_id"],r["title"],"|",r["date_text"])
# discrepancies in title reading for same-date matches
for t in b2:
    if t["entry_id"] in used:
        r=inv[used[t["entry_id"]]]
        if sim(t["title"],r["title"])<0.6: print("TITLE-DIFF",t["entry_id"],t["title"],"<>",r["entry_id"],r["title"],"|",t["date_text"],r["date_text"])
json.dump({k:inv[v]["entry_id"] for k,v in used.items()},open("nb_match.json","w"))
