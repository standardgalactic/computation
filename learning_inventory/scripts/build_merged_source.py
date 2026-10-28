import csv, json, re
ORIG="/mnt/user-data/attachments/d9124a0d-7861-5460-a9c7-29b1bc48ee98/0f26b109-complete_learning_inventory.csv"
rows=list(csv.DictReader(open(ORIG,encoding="utf-8-sig")))
fields=list(rows[0].keys())+["notebook_year","lecturer","lectures_recorded","lectures_listed","date_assumed"]
for r in rows: r.update(notebook_year="",lecturer="",lectures_recorded="",lectures_listed="",date_assumed="")
tx={t["entry_id"]:t for t in csv.DictReader(open("notebook_transcription_2016_2017.csv",encoding="utf-8-sig"))}
match=json.load(open("nb_match.json"))
match["N16-118"]="E342"; match["N16-134"]="E358"
for tid,eid in match.items():
    r=rows[int(eid[1:])-1]; t=tx[tid]
    r["notebook_year"]=t["year"]; r["lecturer"]=t["lecturer"]; r["lectures_recorded"]=t["lectures_recorded"]; r["lectures_listed"]=t["lectures_listed"]; r["date_assumed"]=t["date_assumed"]
# title correction supported by the photo (page of May 28 to Jun 2, 2016)
r=rows[357]; assert r["title"]=="Great Human"
r["title"]="Greek and Roman Technology"
r["notes"]=(r["notes"]+"; " if r["notes"] else "")+"Title corrected from 'Great Human' after checking the notebook photograph (May 30, 2016)"
r=[x for x in rows if x["title"]=="Understanding the Economy" and x["date_text"]=="Jul 7"]; assert len(r)==1; r=r[0]
r["title"]="Understanding the Earth"
r["notes"]=(r["notes"]+"; " if r["notes"] else "")+"Title corrected from 'Understanding the Economy' (confirmed by the user from the notebook, Jul 7, 2016)"
m=[x for x in rows if x["title"]=="Math Is Power"]; assert len(m)==1; m=m[0]
m["notes"]=(m["notes"]+"; " if m["notes"] else "")+"Date corrected from '"+m["date_text"]+"' to 'Mar 20' (confirmed by the user from the notebook)"
m["date_text"]="Mar 20"
# append
append_ids=[t["entry_id"] for t in tx.values() if int(t["sequence_in_batch"])<=81]+["N16-128","N1617-206","N17-226"]
seq=max(int(r["sequence"] or 0) for r in rows if r["source"].startswith("Handwritten"))
added=[]
for tid in append_ids:
    t=tx[tid]; seq+=1
    notes="; ".join(x for x in [("Lecturer: "+t["lecturer"]) if t["lecturer"] else "", ("Format: "+t["format"]) if t["format"] else "", t["notes"]] if x)
    new={k:"" for k in fields}
    new.update(source="Handwritten lecture notebook",source_page="notebook photographs",sequence=str(seq),
        title=t["title"],date_text=t["date_text"],period="Notebook sequence ("+t["year"]+"; added from photographs)",
        kind="Lecture / audiobook / language study",notes=notes,primary_discipline=t["revised_primary_discipline"],
        secondary_discipline="",classification_basis="Manual: assigned from title when transcribed from notebook photographs; "+t["classification_basis"],
        notebook_year=t["year"],lecturer=t["lecturer"],lectures_recorded=t["lectures_recorded"],lectures_listed=t["lectures_listed"],date_assumed=t["date_assumed"])
    rows.append(new); added.append(tid)
with open("merged_source_inventory.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
print(len(rows),"rows;",len(added),"added")
