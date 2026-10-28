import csv, re, collections

CATS = {
 "CS": "Computer Science and Programming",
 "AI": "AI, Machine Learning and Data Science",
 "MA": "Mathematics and Statistics",
 "PH": "Physics and Astronomy",
 "CH": "Chemistry and Materials",
 "BI": "Biology, Neuroscience and Health",
 "ES": "Earth and Environmental Science",
 "EN": "Engineering and Applied Technology",
 "HI": "History",
 "PL": "Philosophy, Logic and Critical Thinking",
 "SO": "Social Sciences and Economics",
 "ED": "Education and Pedagogy",
 "LA": "Languages and Linguistics",
 "AR": "Arts, Music and Literature",
 "GS": "General Science and Interdisciplinary",
}

# (primary, regex on lowercase title, default secondary)
RULES = [
 ("LA", r"^1984|árbol de ciencia|^artículos|diario de che|donde se fue|d'orgeville|ángeles tutelares|la experiencia del dolor|el problema del dolor|leyes de murphy", "AR"),
 ("CS", r"dynamic programming", "MA"),
 ("ED", r"teaching|pedagogy|education|educación|gamification|creating an edx course|utopedia", None),
 ("GS", r"physics of history|complex systems|modern science|36 big ideas|how information grows|shape of nature", None),
 ("ES", r"origin and evolution of earth|geology|how the earth works|planet earth|earth at the crossroads|oceanograph|meteorology|water and climate|sustainable living|ecological planet|gis foundations", None),
 ("CH", r"chemistry|elemental matters|atoms to materials|thermodynamics", "PH"),
 ("LA", r"arabic|spanish|japanese|griego|latino|italian language|french language|pimsleur|michel thomas|berlitz|living languages|linguistic myths", None),
 ("PL", r"language, proof and logic|philosophy|critical thinking|argumentation|science wars|thinking theoretically|everyday thinking|scientific thinking|deceptive mind|joy of thinking|redefining reality", None),
 ("MA", r"matemáticas|math|algebra|calculus|trigonometry|probability|statistics|statistical thinking|estadístic|discrete|optimization|observation theory|fat chance|inference and modeling|linear models|information theory|science of information", None),
 ("AI", r"machine learning|deep learning|neural net|natural language processing|\bnlp\b|text analytics|computer vision|watson|chatgpt|\bai\b|artificial intelligence|chatbots|data science|predictive|statistical learning|statistical predictive|big data|data literacy|analytics|visualizing data|speech recognition|análisis de datos|ciencias de datos|introducción a r|introduction to r |python for data|python basics for data|programming with python for data|foundations of data science|analyzing data|r basics", None),
 ("PH", r"einstein|physics|cosmology|astrophysics|astronomy|relativity|gravity|higgs|dark matter|quantum|nature of matter|stars and|planets and sun|^galaxies|universe|boltzmann|change and motion|perfect theory|^brief history|intelligent life", None),
 ("BI", r"biology|genetic|dna|neuro|brain|human body|anatomy|infectious|history of life|unseen diversity|addiction|vaccin|hearing, touching|science of self|domestication", None),
 ("HI", r"history|civilization|ancient|turning points|middle east|egypt|herodotus|native america|american mind|inventions|innovation|great human", None),
 ("SO", r"economics|economy|anthropology|cultures|understanding diversity|political|socialism|belong|happiness|understanding japan", None),
 ("AR", r"music|how colors|science fiction|george orwell", None),
 ("EN", r"engineering simulations|space mission|embedded|electronics|nanotechnology|acoustics|biomedical|magnetic resonance|image processing|sparse representations|water treatment|sewage|estructuras|signal", None),
 ("CS", r"kubernetes|devops|java|c\+\+|c programming|javascript|node\.js|compilers|linux|unix|shell|python|webassembly|css basics|jenkins|serverless|microservice|cloud|openshift|containers|red hat|data structures|algorithm|database|sql|automata|functional programming|paradigms|object-oriented|how to code|computing|programming|networking|operating systems|blockchain|hyperledger|infrastructure as code|cosmos db|laff|cs50|cs for all|creative coding|computer graphics|procedural modelling|blender|excel", None),
]

# secondary overrides keyed by lowercase title substring
SEC = {
 "big history": "PH", "history of science": "PL", "inventions": "EN", "history of innovation": "EN",
 "history of life": "ES", "ecological planet": "BI", "oceanograph": "BI", "genetics": "MA",
 "music and the brain": "AR", "physics of history": "HI", "complex systems": "MA",
 "how information grows": "SO", "shape of nature": "ES", "modern science": "PL",
 "discrete choice": "SO", "language, proof and logic": "MA", "joy of thinking": "MA",
 "natural language processing": "LA", "text analytics": "LA", "computational neuroscience": "CS",
 "space mission": "PH", "science in art": "AR", "computer graphics": "AR", "blender": "AR",
 "creative coding": "AR", "music technology": "EN", "intelligent life": "BI", "gis foundations": "CS",
 "observation theory": "EN", "mathematical optimization": "EN", "information theory": "CS",
 "science of information": "CS", "laff": "MA", "biomedical": "BI", "magnetic resonance": "BI",
 "image processing and analysis for life": "BI", "water treatment": "ES", "sewage": "ES",
 "antivaccination": "SO", "science of happiness": "BI", "deceptive mind": "SO",
 "everyday thinking": "SO", "political ideas": "PL", "domestication": "HI",
 "data science and agile": "EN", "iot": "EN", "internet of things": "EN",
 "data structures: an active": None, "great human": "BI", "understanding japan": "HI",
 "belong": "HI", "united states and the middle east": "SO", "middle east": "SO",
 "unexpected economics": "HI", "understanding the economy": "HI", "nanotechnology": "CH",
 "thermodynamics": "PH", "elemental matters": "PH", "search for": "BI",
 "dynamic programming": "BI", "introduction to biomedical": "BI",
 "einstein": "PL",
}

def classify(title):
    t = title.lower()
    for cat, rx, sec in RULES:
        if re.search(rx, t):
            s = sec
            for k, v in SEC.items():
                if k in t:
                    s = v
                    break
            if s == cat:
                s = None
            return cat, s
    return None, None

rows = list(csv.DictReader(open("combined_learning_inventory.csv", encoding="utf-8-sig")))
out = []
unmatched = []
for r in rows:
    c, s = classify(r["title"])
    if c is None:
        unmatched.append(r["title"])
        c = "GS"
        note = "Fallback assignment"
    else:
        note = ""
    r["primary_discipline"] = CATS[c]
    r["secondary_discipline"] = CATS[s] if s else ""
    prev = r.get("notes", "")
    basis = "Title-based"
    tl = r["title"].lower()
    if "uncertain" in prev:
        basis += "; uncertain title transcription"
    if c == "LA" and re.search(r"^1984|árbol|^artículos|diario|donde se fue|d'orgeville|ángeles|experiencia del dolor|problema del dolor|leyes de murphy", tl):
        basis += "; Spanish-language reading/listening inferred from title"
    if tl in ("brief history", "great human"):
        basis += "; ambiguous short title"
    r["classification_basis"] = basis
    out.append(r)

fields = list(rows[0].keys())
for f in ("primary_discipline", "secondary_discipline", "classification_basis"):
    if f not in fields:
        fields.append(f)
with open("combined_learning_inventory_classified.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(out)

order = [CATS[k] for k in CATS]
tot = collections.Counter(r["primary_discipline"] for r in out)
nb = collections.Counter(r["primary_discipline"] for r in out if r["source"].startswith("Handwritten"))
ex = collections.Counter(r["primary_discipline"] for r in out if r["source"].startswith("edX"))
sec = collections.Counter(r["secondary_discipline"] for r in out if r["secondary_discipline"])
N = len(out)
with open("discipline_summary.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["primary_discipline", "total", "percent_of_total", "notebook", "edX", "also_secondary"])
    for d in sorted(order, key=lambda d: -tot[d]):
        w.writerow([d, tot[d], f"{100*tot[d]/N:.1f}", nb[d], ex[d], sec[d]])
    w.writerow(["TOTAL", N, "100.0", sum(nb.values()), sum(ex.values()), ""])

print("unmatched:", unmatched)
for d in sorted(order, key=lambda d: -tot[d]):
    print(f"{d}: {tot[d]} (nb {nb[d]}, edX {ex[d]}, sec {sec[d]})")
print()
for d in order:
    print("==", d)
    seen = []
    for r in out:
        if r["primary_discipline"] == d and r["title"] not in seen:
            seen.append(r["title"])
    print(" | ".join(x[:45] for x in seen))
