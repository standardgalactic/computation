import csv, re, json, os, collections

SRC = "/home/claude/work/merged_source_inventory.csv"
N_ORIGINAL = 481
OUT = "/home/claude/work"
os.makedirs(OUT, exist_ok=True)

PS = "Psychology and Cognitive Science"
BI = "Biology, Neuroscience and Health"
AR = "Arts, Music and Literature"
LA = "Languages and Linguistics"
PL = "Philosophy, Logic and Critical Thinking"
SO = "Social Sciences and Economics"
HI = "History"
MA = "Mathematics and Statistics"
CS = "Computer Science and Programming"
AI = "AI, Machine Learning and Data Science"
PH = "Physics and Astronomy"
CH = "Chemistry and Materials"
ES = "Earth and Environmental Science"
EN = "Engineering and Applied Technology"
ED = "Education and Pedagogy"
GS = "General Science and Interdisciplinary"

LABEL_NORMALIZATION = {"Arts, Literature and Music": AR}

SHORT = {
    PS: "Psychology and Cognition", BI: "Biology and Health", AR: "Arts and Literature",
    LA: "Languages and Linguistics", PL: "Philosophy and Logic", SO: "Social Sciences",
    HI: "History", MA: "Mathematics and Statistics", CS: "Computer Science",
    AI: "AI and Data Science", PH: "Physics and Astronomy", CH: "Chemistry",
    ES: "Earth Science", EN: "Engineering", ED: "Education", GS: "Interdisciplinary",
}

# ---------------------------------------------------------------------------
# Primary reassignments (title regex, course-code regex, new primary, reason)
# ---------------------------------------------------------------------------
PRIMARY_RULES = [
    (None, r"^PSYC", PS, "Psychology course identified by course code PSYC"),
    (r"music and the brain", None, PS, "Music cognition; title names brain and music perception"),
    (r"hearing, touching, tasting", None, PS, "Sensory perception"),
    (r"how colors affect you", None, PS, "Psychology of color perception"),
    (r"deceptive mind", None, PS, "Cognitive biases and reasoning errors; critical thinking kept as secondary"),
    (r"science of everyday thinking", None, PS, "Cognitive science of reasoning"),
    (r"science of happiness", None, PS, "Psychology of well-being"),
    (r"^effective oral communications", None, LA, "Communication skills course; not a pedagogy course"),
    (r"^understanding the earth$", None, ES, "Title corrected from Understanding the Economy; earth science"),
    (r"^greek and roman technology$", None, HI, "Title corrected from Great Human; history of technology"),
    (r"^brief history$", None, HI, "Identified as Stearns, A Brief History of the World (Great Courses, 36 lectures); world history, not physics"),
]

# ---------------------------------------------------------------------------
# Secondary assignments. A secondary is given only where the title itself names
# or plainly implies a second domain. Everything else is left empty.
# (title regex, secondary, reason)
# ---------------------------------------------------------------------------
SECONDARY_RULES = [
    (r"^1984", AR, "Novel by Orwell; literary work, independent of the language of the recording"),
    (r"árbol de ciencia", AR, "Novel (title transcription uncertain)"),
    (r"diario de che", HI, "Revolutionary diary; historical document"),
    (r"el problema del dolor", PL, "C. S. Lewis on suffering; philosophical and theological argument"),
    (r"^big history", PH, "Course spans cosmic and human history"),
    (r"^inventions|history of innovation", EN, "History of technology"),
    (r"^ecological planet", BI, "Ecology"),
    (r"physics of history", HI, "Title names history"),
    (r"intelligent life", BI, "Astrobiology"),
    (r"science in art", AR, "Title names art"),
    (r"blender|creative coding", AR, "3D animation and creative practice"),
    (r"music technology", EN, "Title names technology"),
    (r"natural language processing|text analytics", LA, "Title names natural language"),
    (r"speech recognition", LA, "Speech and language"),
    (r"language, proof and logic|symbolic logic", MA, "Formal logic"),
    (r"discrete choice", SO, "Econometric choice modeling"),
    (r"information theory|science of information", CS, "Information theory underlies computing and communication"),
    (r"laff-on", MA, "Linear algebra foundations (LAFF)"),
    (r"mathematical optimization for engineers", EN, "Title names engineers"),
    (r"mathematical and computational methods|scientific visualization", CS, "Title names computation or visualization"),
    (r"boltzmann", CS, "Title names computing"),
    (r"embedded systems", CS, "Microcontroller programming"),
    (r"computational neuroscience", PS, "Title names cognition"),
    (r"understanding the brain|^addiction", PS, "Brain and behavior"),
    (r"biomedical imaging|image processing and analysis for life|magnetic resonance", BI, "Biomedical application"),
    (r"water treatment|sewage", ES, "Environmental application"),
    (r"data science and agile|\biot\b|internet of things", EN, "Systems and device engineering"),
    (r"big data and education", AI, "Title names big data"),
    (r"gis foundations", CS, "Geographic information systems software"),
    (r"dynamic programming", BI, "Title names genomics"),
    (r"thermodynamics and phase|from atoms to materials", PH, "Physical foundations"),
    (r"nanotechnology", CH, "Materials at the nanoscale"),
    (r"greek and roman technology", EN, "Title names technology"),
    (r"albert einstein", PL, "Title names philosopher"),
    (r"domestication", HI, "Human prehistory"),
    (r"great human", BI, "Human evolution (title transcription uncertain)"),
    (r"united states and the middle east|middle east, 1914", SO, "International politics"),
    (r"political ideas", PL, "Political thought"),
    (r"antivaccination", SO, "Social dimension of hesitancy"),
    (r"music and the brain", AR, "Music"),
    (r"how colors", AR, "Color in art and design"),
    (r"deceptive mind", PL, "Critical thinking"),
    (r"everyday thinking", PL, "Reasoning"),
    (r"philosophies of mind", PS, "Philosophy of mind meets cognitive science"),
    (r"history of psychology", HI, "Title names history"),
    (r"statistical analysis in psychology", MA, "Statistics"),
    (r"social psychology", SO, "Social behavior"),
    (r"physiological psychology|health psychology", BI, "Physiological or health content"),
    (r"second language education|esl education|field experience in tesl", LA, "Language teaching"),
]

# ---------------------------------------------------------------------------
# Interpretive themes. Keyword based and non-exclusive; independent of the
# discipline labels.
# ---------------------------------------------------------------------------
THEMES = [
    ("Information", r"information|big data|data science|ciencias de datos|data literacy|analytics|predictive analytics|predictive model|signal|sparse representations|boltzmann|genetic code|genomics|speech recognition|computer vision|image processing|imaging|database|sql|data analysis|análisis de datos|magnetic resonance|acoustics"),
    ("Constraint and Optimization", r"optimization|thermodynamics|phase equilibria|dynamic programming|boltzmann|discrete choice|observation theory|estructuras|water treatment|sewage|sustainable living|space mission"),
    ("Evolution and Development", r"rise of humans|abiogenesis|archeology|biology and human|evolution|history of life|big history|origin|domestication|child development|prehistory|great human|ecolog|language change|physics of history|genetic|genetics|dna|genomics|inventions|innovation|intelligent life"),
    ("Mind and Cognition", r"consciousness|memory and the|being human|human behavio|psychology of|passions|emotions|cognitive behavioral|memory|psycholog|personality|cognitive|cognition|perception|\bbrain\b|neuro|philosophies of mind|critical thinking|everyday thinking|scientific thinking|joy of thinking|thinking theoretically|deceptive mind|hearing, touching|colors affect|^learning$|happiness|^addiction"),
    ("Computation", r"programming|python|java\b|c\+\+|javascript|algorithm|compilers|automata|computing|computer|software|devops|kubernetes|linux|unix|shell|cloud|data structures|blockchain|hyperledger|node\.js|webassembly|functional|paradigms|machine learning|deep learning|neural|artificial intelligence|\bai\b|nlp|natural language|embedded|computational|\bexcel\b|information theory|how to code|infrastructure as code|\bcss\b|jenkins|networking|microservice|cosmos db|game development|gis foundations|introducción a r|chatgpt|chatbots|watson"),
    ("Language and Meaning", r"sentences|conversation|communication skills|rhetoric|blancanieves|analysis & critique|role of the author|language|linguistic|phonetics|arabic|spanish|japanese|french|italian|latin|latino|griego|michel thomas|pimsleur|berlitz|paul noble|speech recognition|text analytics|literature|argumentation|communications"),
    ("Formal Reasoning", r"geometry|game theory|mental math|high school math|logic|proof|calculus|algebra|discrete|probability|statistic|estadístic|statistical|inference|math|matemáticas|trigonometry|automata|propositional|observation theory|fat chance|research methods"),
    ("Machine Learning", r"(machine|deep|statistical|reinforcement) learning(?!.*pedagog)|ml for|supervised learning"),
    ("Learning and Education", r"active learning|^learning$|pedagog|teaching|education|educación|tesl|esl |gamification|changing behaviour"),
    ("Complex Systems", r"complex systems|ecolog|dynamics|climate|meteorology|oceanograph|how the earth works|economics|economy|big history|shape of nature|earth at the crossroads|planet earth|sustainable"),
    ("Physical Structure and Scale", r"superstring|entanglement|cosmology|gravity|higgs|dark matter|quantum|nature of matter|universe|astro|stars|galaxies|planets|relativity|(?<!meta)physics|change and motion|perfect theory|elemental|chemistry|atoms|materials|nanotechnology|thermodynamics|einstein"),
    ("Modeling and Simulation", r"simulation|modelling|modeling|procedural|scientific visualization|graphics|blender|creative coding"),
    ("Knowledge and Method", r"existentialism|natural law|modern mind|quest for meaning|angelic doctor|from plato|science in the twentieth|scientific ideas that changed|^reality$|philosoph|science wars|redefining reality|metaphysics|epistemology|scientific thinking|critical thinking|research methods|argumentation|history of science|modern science|36 big ideas|question everything|everyday thinking|deceptive mind|joy of thinking|thinking theoretically"),
    ("History and Society", r"buddhism|new testament|mythology|african experience|money and banking|conflict management|negotiation|courtroom|how ideas spread|^god$|archeology|modern mind|twentieth century|(?<!big )(?<!physics of )history(?! of life)(?! of science)|civiliz|anthropology|sociolog|society|social psychology|political|economics|economy|cultures|understanding diversity|middle east|japan|native america|american mind|egypt|herodotus|ancient|socialism|belong|latin american|mexican|greek myth|religion"),
]

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
assert len(rows) >= N_ORIGINAL

out_rows, changes, theme_rows = [], [], []
for i, r in enumerate(rows, 1):
    eid = f"E{i:03d}"
    t = r["title"].lower()
    code = r.get("course_code", "") or ""
    op = r["primary_discipline"]
    oq = r["secondary_discipline"]

    # primary
    added = i > N_ORIGINAL
    np_, preason = LABEL_NORMALIZATION.get(op, op), ""
    if np_ != op:
        preason = "Label normalization"
    for tre, cre, newp, reason in ([] if added else PRIMARY_RULES):
        if (tre is None or re.search(tre, t)) and (cre is None or re.search(cre, code)) and (tre or cre):
            np_, preason = newp, reason
            break

    # secondary
    nq, qreason = "", ""
    for tre, sec, reason in SECONDARY_RULES:
        if re.search(tre, t):
            if sec != np_:
                nq, qreason = sec, reason
            break

    # themes
    tags = []
    for name, rx in THEMES:
        m = re.search(rx, t)
        if m:
            tags.append(name)
            theme_rows.append({"entry_id": eid, "source": r["source"], "title": r["title"],
                               "primary_discipline": np_, "theme": name, "matched_term": m.group(0)})

    new = {"entry_id": eid}
    for k in ["source","source_page","sequence","title","date_text","period","kind","notes",
              "course_code","grade","credit_hours","grade_points","record_status","academic_year","term",
              "notebook_year","lecturer","lectures_recorded","lectures_listed","date_assumed"]:
        new[k] = r.get(k, "")
    new["original_primary_discipline"] = "" if added else op
    new["original_secondary_discipline"] = "" if added else oq
    new["original_classification_basis"] = "" if added else r.get("classification_basis", "")
    new["revised_primary_discipline"] = np_
    new["revised_secondary_discipline"] = nq
    new["revision_basis"] = ("Added from notebook photographs; primary assigned from title" if added else (preason or "Unchanged")) + ("; secondary: " + qreason if qreason else "")
    new["themes"] = "; ".join(tags)
    out_rows.append(new)

    for field, old, nw, why in (() if added else (("primary", op, np_, preason or ""),
                                ("secondary", oq, nq, qreason or "No defensible second domain from the title"))):
        if old != nw:
            changes.append({"entry_id": eid, "source": r["source"], "title": r["title"],
                            "field": field, "old_value": old, "new_value": nw, "reason": why})

def write(name, rows_, fields=None):
    fields = fields or list(rows_[0].keys())
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows_)

write("complete_learning_inventory_revised.csv", out_rows)
write("classification_change_log.csv", changes)
write("theme_assignments.csv", theme_rows)

# ---------------- discipline network ----------------
disc = sorted({r["revised_primary_discipline"] for r in out_rows} |
              {r["revised_secondary_discipline"] for r in out_rows if r["revised_secondary_discipline"]})
SK = {"University of New Brunswick transcript": "university",
      "Handwritten lecture notebook": "notebook", "edX dashboard": "edx"}
nodes = []
for d in disc:
    ents = [r for r in out_rows if r["revised_primary_discipline"] == d]
    cnt = collections.Counter(SK[r["source"]] for r in ents)
    nodes.append({"discipline": d, "entries": len(ents),
                  "secondary_mentions": sum(1 for r in out_rows if r["revised_secondary_discipline"] == d),
                  "university": cnt["university"], "notebook": cnt["notebook"], "edx": cnt["edx"]})
nodes.sort(key=lambda n: -n["entries"])
write("discipline_network_nodes.csv", nodes)

pairs = collections.defaultdict(list)
for r in out_rows:
    if r["revised_secondary_discipline"]:
        k = tuple(sorted([r["revised_primary_discipline"], r["revised_secondary_discipline"]]))
        pairs[k].append(r["title"])
edges = []
for (a, b), titles in pairs.items():
    uniq = list(dict.fromkeys(titles))
    edges.append({"discipline_a": a, "discipline_b": b, "shared_classified_entries": len(titles),
                  "distinct_titles": len(uniq), "example_courses": "; ".join(uniq[:8])})
edges.sort(key=lambda e: -e["shared_classified_entries"])
write("discipline_network_edges.csv", edges)

# ---------------- thematic network ----------------
tn = []
for name, _ in THEMES:
    tr = [x for x in theme_rows if x["theme"] == name]
    cnt = collections.Counter(SK[x["source"]] for x in tr)
    dd = collections.Counter(x["primary_discipline"] for x in tr)
    tn.append({"theme": name, "entries": len(tr), "university": cnt["university"], "notebook": cnt["notebook"],
               "edx": cnt["edx"], "disciplines_spanned": len(dd),
               "top_disciplines": "; ".join(f"{k} ({v})" for k, v in dd.most_common(4))})
tn.sort(key=lambda n: -n["entries"])
write("thematic_network_nodes.csv", tn)

bytheme = collections.defaultdict(set)
for x in theme_rows:
    bytheme[x["entry_id"]].add(x["theme"])
title_of = {r["entry_id"]: r["title"] for r in out_rows}
co = collections.defaultdict(list)
for eid, ths in bytheme.items():
    for a in ths:
        for b in ths:
            if a < b:
                co[(a, b)].append(title_of[eid])
te = []
for (a, b), titles in co.items():
    uniq = list(dict.fromkeys(titles))
    te.append({"theme_a": a, "theme_b": b, "shared_entries": len(titles), "distinct_titles": len(uniq),
               "example_courses": "; ".join(uniq[:8])})
te.sort(key=lambda e: -e["shared_entries"])
write("thematic_network_edges.csv", te)

untagged = [r["title"] for r in out_rows if not r["themes"]]
data = {
    "entries": [{"t": r["title"], "s": SK[r["source"]][0].upper(),
                 "p": r["revised_primary_discipline"], "q": r["revised_secondary_discipline"],
                 "th": [x for x in r["themes"].split("; ") if x]} for r in out_rows],
    "short": SHORT, "themes": [n for n, _ in THEMES],
}
json.dump(data, open(os.path.join(OUT, "data.json"), "w"), ensure_ascii=False)

print("rows", len(out_rows), "changes", len(changes), "untagged themes", len(untagged))
print(collections.Counter(r["revised_primary_discipline"] for r in out_rows).most_common())
print("with secondary:", sum(1 for r in out_rows if r["revised_secondary_discipline"]))
print(collections.Counter((c["field"]) for c in changes))
print("TOP DISC EDGES"); [print(e["shared_classified_entries"], e["discipline_a"], "|", e["discipline_b"]) for e in edges[:12]]
print("THEMES"); [print(n["entries"], n["theme"], n["disciplines_spanned"]) for n in tn]
print("TOP THEME EDGES"); [print(e["shared_entries"], e["theme_a"], "|", e["theme_b"]) for e in te[:10]]
