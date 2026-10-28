import csv, collections, re

PS = "Psychology and Cognitive Science"; BI = "Biology, Neuroscience and Health"
AR = "Arts, Music and Literature"; LA = "Languages and Linguistics"
PL = "Philosophy, Logic and Critical Thinking"; SO = "Social Sciences and Economics"
HI = "History"; MA = "Mathematics and Statistics"; PH = "Physics and Astronomy"
CH = "Chemistry and Materials"; ES = "Earth and Environmental Science"
EN = "Engineering and Applied Technology"; ED = "Education and Pedagogy"
GS = "General Science and Interdisciplinary"; CS = "Computer Science and Programming"
AI = "AI, Machine Learning and Data Science"
N = ""

# (title, creator, date, year, format, notes, primary, secondary)
Y6, Y7 = "2016", "2017"
R = [
 # ---- 2016, Mar 22 onward
 ("Inventions", "", "Mar 22", Y6, "", "", EN, HI),
 ("Math is Power", "", "Mar 20", Y6, "", "Date confirmed by the user as Mar 20, although the line sits after the Mar 22 entry on the page", MA, N),
 ("Ecological Planet", "", "Mar 24", Y6, "", "", ES, BI),
 ("Addiction", "", "Mar 25", Y6, "", "", PS, BI),
 ("Earth at the Crossroads", "", "Mar 25", Y6, "", "Below a ruled line", ES, N),
 ("Gravity", "", "Mar 26", Y6, "", "", PH, N),
 ("Modern History", "", "Mar 27", Y6, "", "", HI, N),
 ("Cosmology", "", "Mar 29", Y6, "", "Blue ink; margin note (az)", PH, N),
 ("Science of Self: Genetics", "", "Mar 30", Y6, "", "", BI, N),
 ("Oceanography", "", "Apr 1", Y6, "", "", ES, N),
 ("Information Theory", "", "Apr 3", Y6, "", "", CS, MA),
 ("Unexpected Economics", "", "Apr 4", Y6, "", "", SO, N),
 ("History of Life", "", "Apr 6", Y6, "", "Reading confirmed by the user (first word heavily flourished)", BI, HI),
 ("Shape of Nature", "", "Apr 9", Y6, "", "", ES, GS),
 ("Art of Teaching", "", "Apr 10", Y6, "", "", ED, N),
 ("Algebra I", "", "Apr 12", Y6, "", "", MA, N),
 ("Algebra II", "", "Apr 13", Y6, "", "Green ink", MA, N),
 ("Discrete Math", "", "Apr 14", Y6, "", "", MA, N),
 ("History of Native Americans", "", "Apr 15", Y6, "", "Last word cut off (American)", HI, N),
 ("Thinking Theoretically", "", "Apr 18", Y6, "", "", PL, N),
 ("Understanding Japan", "", "Apr 23", Y6, "", "", HI, SO),
 ("Japanese Foundations", "Michel Thomas", "Apr 29", Y6, "Language course", "Michel Thomas Method", LA, N),
 ("History of Life", "", "May 2", Y6, "", "", BI, HI),
 ("Comparative Education", "", "May 3", Y6, "", "", ED, SO),
 ("Cosmology", "", "May 4", Y6, "", "", PH, N),
 ("Nature of Matter", "", "May 5", Y6, "", "", CH, PH),
 ("The Origin and Evolution of Earth", "", "May 7", Y6, "", "", ES, N),
 ("Hearing, Touching, Tasting", "", "May 8", Y6, "", "Prefix before title unclear", PS, BI),
 ("The Higgs Boson and Beyond", "", "May 9", Y6, "", "", PH, N),
 ("Modern Physics for Non-Scientists", "", "May 10", Y6, "", "", PH, N),
 ("Physics in Your Life", "", "May 12", Y6, "", "", PH, N),
 ("High School Chemistry", "", "May 13", Y6, "", "", CH, N),
 ("Oceanography", "", "May 15", Y6, "", "", ES, N),
 ("Addiction", "", "May 16", Y6, "", "", PS, BI),
 ("Peoples and Cultures of the World", "Edward Fischer", "May 17", Y6, "", "", SO, HI),
 ("Albert Einstein: Physicist, Philosopher, Humanitarian", "Don Howard", "May 17", Y6, "", "", PL, PH),
 ("1984", "George Orwell", "May 18", Y6, "Spanish audiobook (0.7x speed)", "Under the heading español", LA, AR),
 ("El árbol de la ciencia", "(James, as written)", "May 19", Y6, "Spanish audiobook", "Author field reads James; uncertain", LA, AR),
 ("Artículos", "Del Valle", "May 19", Y6, "Spanish audio", "", LA, N),
 ("Diario del Che", "Guevara", "May 19", Y6, "Spanish audiobook", "", LA, HI),
 ("Donde se fue el fuego", "Guevara", "May 19", Y6, "Spanish audiobook", "Title reading uncertain", LA, AR),
 ("D'Orgeville", "Sade", "May 19", Y6, "Spanish audiobook", "Title reading uncertain", LA, AR),
 ("Ángeles tutelares", "", "May 20", Y6, "Spanish audiobook", "", LA, AR),
 ("La experiencia del dolor", "", "", Y6, "Spanish audiobook", "No date", LA, N),
 ("El problema del dolor", "C. S. Lewis", "", Y6, "Spanish audiobook", "No date; author in parentheses", LA, PL),
 ("Las leyes de Murphy", "", "", Y6, "Spanish audiobook", "No date", LA, N),
 ("Blancanieves, Pulgarcito...", "", "", Y6, "Spanish audiobook", "Fairy tales; No date", LA, AR),
 ("Cosmology", "", "May 24", Y6, "", "Underlined", PH, N),
 ("Understanding Gravity", "", "May 25", Y6, "", "", PH, N),
 ("Dark Matter and Energy", "", "May 26", Y6, "", "", PH, N),
 ("Big History", "", "May 27", Y6, "", "", HI, PH),
 ("Physics of History", "", "May 28", Y6, "", "", GS, HI),
 ("Greek and Roman Technology", "", "May 30", Y6, "", "Red ink", HI, EN),
 ("Physics and Our Universe", "", "Jun 1", Y6, "", "", PH, N),
 ("How Colors Affect You", "", "Jun 2", Y6, "", "", PS, N),
 ("The Higgs Boson and Beyond", "", "Jun 2", Y6, "", "", PH, N),
 ("Music and the Brain", "", "Jun 3", Y6, "", "", PS, AR),
 ("Understanding the Universe (Introduction to Astronomy)", "", "Jun 7", Y6, "", "Blue ink date", PH, N),
 ("Organic Chemistry", "", "Jun 8", Y6, "", "", CH, N),
 ("History of Life", "", "Jun 9", Y6, "", "", BI, HI),
 ("History of Ancient Israel", "", "Jun 10", Y6, "", "", HI, N),
 ("Ancient and Medieval History", "", "Jun 11", Y6, "", "", HI, N),
 ("The Human Factor: Domestication", "", "Jun 12", Y6, "", "", BI, HI),
 ("Unseen Diversity", "", "Jun 12", Y6, "", "", BI, N),
 ("Elemental Matters", "", "Jun 13", Y6, "", "Date partly illegible", CH, N),
 ("Nature of Matter", "", "Jun 14", Y6, "", "Date partly illegible", CH, PH),
 ("Science Wars", "", "Jun 15", Y6, "", "", PL, SO),
 ("Science Fiction: Literature and Technology", "", "Jun 15", Y6, "", "Subtitle overwritten (imagination?)", AR, GS),
 ("Your Deceptive Mind", "", "Jun 16", Y6, "", "", PS, N),
 ("Big Data", "", "Jun 17", Y6, "", "", AI, N),
 ("Ecological Planet", "", "Jun 18", Y6, "", "", ES, BI),
 ("Human Body", "", "Jun 19", Y6, "", "", BI, N),
 ("Nanotechnology", "", "Jun 20", Y6, "", "", EN, CH),
 ("Science of Information", "", "Jun 22", Y6, "", "", CS, MA),
 ("Understanding the Brain", "", "Jun 30", Y6, "", "Brown ink", BI, PS),
 ("History of Innovation", "", "Jul 1", Y6, "", "Brown ink", HI, EN),
 ("Precalculus and Trigonometry", "", "Jul 4", Y6, "", "", MA, N),
 ("Your Deceptive Mind: Critical Thinking", "", "Jul 5", Y6, "", "", PS, PL),
 ("Understanding Japan", "", "Jul 6", Y6, "", "", HI, SO),
 ("Understanding the Earth", "", "Jul 7", Y6, "", "Brown ink", ES, N),
 ("Planets and the Sun", "", "Jul 10", Y6, "", "", PH, N),
 ("Stars and Galaxies", "", "Jul 11", Y6, "", "", PH, N),
 ("The Terror of History: Mystics, Heretics, and Witch Burners", "", "Jul 12", Y6, "", "Subtitle reading uncertain", HI, N),
 ("History of Science: Antiquity", "", "Jul 13", Y6, "", "", HI, N),
 ("History of Science: 1700-1900", "", "Jul 14", Y6, "", "", HI, N),
 ("Big History", "", "Jul 19", Y6, "", "", HI, PH),
 ("Human Prehistory and the First Civilizations", "", "Jul 20", Y6, "", "", HI, N),
 ("Precalculus and Trigonometry", "", "Jul 21", Y6, "", "Date partly illegible", MA, N),
 ("Japanese Foundations", "Michel Thomas", "Jul 21", Y6, "Language course", "Marked MT", LA, N),
 ("Change and Motion", "", "Jul 22", Y6, "", "", MA, N),
 ("History of Egypt", "", "Jul 24", Y6, "", "", HI, N),
 ("Herodotus' History", "Herodotus", "Jul 26", Y6, "", "", HI, AR),
 ("Cosmology", "", "Jul 27", Y6, "", "Underlined", PH, N),
 ("Political Ideas", "", "Jul 28", Y6, "", "", SO, PL),
 ("High School Chemistry", "", "Jul 30", Y6, "", "", CH, N),
 ("Turning Points in Modern History", "", "Aug 2", Y6, "", "", HI, N),
 ("Human Body", "", "Aug 4", Y6, "", "", BI, N),
 ("Power of Math", "", "Aug 6", Y6, "", "Pink ink; numbered 1 in margin", MA, N),
 ("Elemental Matters", "", "Aug 10", Y6, "", "Pink ink; numbered 2 in margin", CH, N),
 ("Understanding Modern Electronics", "", "Aug 13", Y6, "", "", EN, PH),
 ("Cosmology", "", "Aug 15", Y6, "", "Underlined; date partly illegible", PH, N),
 ("Geology: Origin and Evolution of Earth", "", "Aug 18", Y6, "", "", ES, N),
 ("Unseen Diversity: Bacteria", "", "Aug 20", Y6, "", "", BI, N),
 ("The Joy of Thinking", "", "Aug 22", Y6, "", "", PL, MA),
 ("History of Life", "", "Aug 24", Y6, "", "", BI, HI),
 ("Arabic", "", "", Y6, "Language study", "Heading; margin bracket from Aug 6 onward", LA, N),
 # ---- 2016 autumn language block
 ("Linguistic Myths", "", "Sep 23", Y6, "", "", LA, N),
 ("Egyptian Arabic", "Michel Thomas", "", Y6, "Language course", "No date", LA, N),
 ("Living Languages: Arabic", "", "", Y6, "Language course", "No date", LA, N),
 ("50 Languages: Arabic", "", "", Y6, "Language course", "No date", LA, N),
 ("Berlitz Arabic", "Berlitz", "", Y6, "Language course", "No date", LA, N),
 ("Quantum Physics", "", "Oct 14", Y6, "", "Blue ink", PH, N),
 ("Arabic on the Move", "", "", Y6, "Language course", "No date", LA, N),
 ("Elemental Matters", "", "Oct 20", Y6, "", "", CH, N),
 ("Spanish", "Michel Thomas", "Oct 22", Y6, "Language course", "", LA, N),
 ("Spanish", "Paul Noble", "Oct 23", Y6, "Language course", "", LA, N),
 ("Egyptian Arabic", "Pimsleur", "Oct 25", Y6, "Language course", "", LA, N),
 ("Cosmology", "", "Nov 1", Y6, "", "Pink ink", PH, N),
 ("Arabic", "Michel Thomas", "Nov 5", Y6, "Language course", "", LA, N),
 ("50 Languages: Arabic", "", "Nov 6", Y6, "Language course", "", LA, N),
 ("Japanese", "Michel Thomas", "Nov 11", Y6, "Language course", "", LA, N),
 ("Eastern Arabic I", "", "Nov 15", Y6, "Language course", "", LA, N),
 ("Ecological Planet", "", "Nov 21", Y6, "", "Top of next page", ES, BI),
 ("50 Languages: Arabic", "", "", "2016-2017", "Language course", "No date; underlined in blue", LA, N),
 ("Arabic", "", "", "2016-2017", "Language course", "No date", LA, N),
 ("Great Ideas of Classical Physics", "", "", "2016-2017", "", "No date; underlined; precedes a ruled line", PH, N),
 # ---- 2017
 ("The United States and the Middle East, 1914-2001", "", "Jan 27 to Feb 2(?)", Y7, "", "Boxed date; second date overwritten; year 2017", HI, SO),
 ("Arabic (Egypt)", "Michel Thomas", "Feb 2", Y7, "Language course", "Marked MT", LA, N),
 ("Redefining Reality", "", "Feb 13", Y7, "", "Dark red ink", PL, PH),
 ("Modern Science", "", "Feb 15", Y7, "", "Red ink", GS, PL),
 ("Big History", "", "Feb 18", Y7, "", "Red ink", HI, PH),
 ("Argumentation", "", "Feb 19", Y7, "", "", PL, N),
 ("Classical Physics", "", "Feb 20", Y7, "", "", PH, N),
 ("History of Life", "", "Feb 20", Y7, "", "", BI, HI),
 ("Cultural Anthropology", "", "Feb 21", Y7, "", "", SO, N),
 ("Physics of History", "", "Feb 22", Y7, "", "", GS, HI),
 ("Physics in Your Life (Everyday Physics)", "", "Feb 23", Y7, "", "", PH, N),
 ("The Search for Intelligent Life", "", "Feb 24", Y7, "", "", PH, BI),
 ("How the Earth Works", "", "Mar 1", Y7, "", "", ES, N),
 ("Philosophy of Science", "", "", Y7, "", "No date; blue ink", PL, GS),
 ("The Higgs Boson and Beyond", "", "", Y7, "", "No date; blue ink", PH, N),
 ("Sustainable Living", "", "", Y7, "", "No date; blue ink", ES, N),
 ("Understanding Diversity", "", "", Y7, "", "No date; word Diversity overwritten", SO, N),
 ("Infectious Diseases", "", "Mar 10", Y7, "", "", BI, N),
 ("Probability", "", "", Y7, "", "No date", MA, N),
 ("Oceanography", "", "", Y7, "", "No date; struck through, with red reversed writing (Modern Science? Big History) over it", ES, N),
 ("Meteorology", "", "", Y7, "", "No date; struck through with red reversed writing", ES, N),
 ("Genetics", "", "", Y7, "", "No date; very faint", BI, N),
 ("Complex Systems", "", "Apr 1", Y7, "", "", GS, MA),
 ("Human Anatomy", "", "Apr 2", Y7, "", "", BI, N),
 ("History of Science: Antiquity to 1700", "", "Apr 4", Y7, "", "", HI, N),
 ("History of Science: 1700-1900", "", "Apr 8", Y7, "", "", HI, N),
 ("The American Mind", "", "Apr 11", Y7, "", "Word before title struck out", HI, PL),
 ("Physics in Your Life", "", "Apr 12", Y7, "", "Blue ink", PH, N),
 ("Physics of History", "", "Apr 13", Y7, "", "Blue ink", GS, HI),
 ("Philosophy of Science", "", "Apr 20", Y7, "", "Reading uncertain; smudged", PL, GS),
 ("Nature of Matter", "", "Apr 24", Y7, "", "Smudged", CH, PH),
 ("How the Earth Works", "", "May 1", Y7, "", "Blue ink; overwritten", ES, N),
 ("Inventions", "", "May 12", Y7, "", "", EN, HI),
 ("Nature of Matter", "", "May 19", Y7, "", "", CH, PH),
 ("Planet Earth", "", "May 20", Y7, "", "", ES, N),
 ("Higgs Boson", "", "May 21", Y7, "", "Faint", PH, N),
 ("Big History", "", "May 23", Y7, "", "", HI, PH),
 ("The Perfect Theory", "", "May 25", Y7, "", "", PH, N),
 ("36 Big Ideas", "", "May 28", Y7, "", "Faint", GS, N),
 ("How Information Grows", "", "Jun 1", Y7, "", "Faint", GS, SO),
 ("Physics of History", "", "Jun 5", Y7, "", "", GS, HI),
 ("Brief History", "Peter N. Stearns", "Jun 7", Y7, "Lecture series", "Blue ink; repeat of the Jan 5, 2016 course (A Brief History of the World, 36 lectures, confirmed from the product page)", HI, N),
 ("Dark Matter and Energy", "", "Jun 9", Y7, "", "Blue ink", PH, N),
 ("Earth at the Crossroads", "", "Jun 10", Y7, "", "Blue ink", ES, N),
 ("Ecological Planet", "", "Jun 11", Y7, "", "Blue ink", ES, BI),
 ("Stars and Planets", "", "Jun 12", Y7, "", "", PH, N),
 ("Galaxies", "", "Jun 14", Y7, "", "", PH, N),
 ("The Joy of Thinking", "", "Jun 15", Y7, "", "", PL, MA),
 ("Modern Science", "", "Jun 17", Y7, "", "", GS, PL),
 ("Science Wars", "", "Jun 18", Y7, "", "", PL, SO),
]

AMBIG_NOTE = re.compile(r"uncertain|illegible|unclear|struck|overwritten|reading|faint|smudged|cut off", re.I)

base = list(csv.DictReader(open("/home/claude/work/notebook_2016_early_pages.csv", encoding="utf-8-sig")))
fields = list(base[0].keys()) + ['date_assumed']
for _r in base: _r['date_assumed'] = ''
rows = list(base)
n = len(base)
for (t, who, d, y, fmt, note, p, q) in R:
    n += 1
    assumed = ""
    if y == Y7 and not d:
        if t in ("Philosophy of Science", "The Higgs Boson and Beyond", "Sustainable Living", "Understanding Diversity"):
            d, assumed = "undated (between Mar 1 and Mar 10)", "Mar 1"
        elif t in ("Probability", "Oceanography", "Meteorology", "Genetics"):
            d, assumed = "undated (between Mar 10 and Apr 1)", "Apr 1"
    if assumed:
        note = (note + "; " if note else "") + "Working date " + assumed + " assigned on the user's instruction; written order places it in the window shown"
    basis = "Title based"
    if who: basis += " and creator"
    if AMBIG_NOTE.search(note) or AMBIG_NOTE.search(t): basis += "; ambiguous or uncertain"
    if not d: basis += "; undated"
    per = {"2016": "Notebook 2016", "2017": "Notebook 2017", "2016-2017": "Notebook late 2016 to early 2017"}[y]
    rows.append({"entry_id": f"{'N16' if y=='2016' else 'N17' if y=='2017' else 'N1617'}-{n:03d}",
                 "source": "Handwritten lecture notebook", "sequence_in_batch": n, "title": t, "lecturer": who,
                 "date_text": d, "date_assumed": assumed, "year": y, "period": per, "format": fmt, "lectures_recorded": "", "lectures_listed": "36" if t=="Brief History" else "", "notes": note,
                 "revised_primary_discipline": p, "revised_secondary_discipline": q, "classification_basis": basis})

out = "/home/claude/work/notebook_transcription_2016_2017.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

print("batch 2 rows:", len(R), "| merged rows:", len(rows))
print("by year:", dict(collections.Counter(r["year"] for r in rows)))
print("undated:", sum(1 for r in rows if not r["date_text"]), "| uncertain:", sum("uncertain" in r["classification_basis"] for r in rows))
for k, v in collections.Counter(r["revised_primary_discipline"] for r in rows).most_common(): print(f"{v:4d} {k}")

def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
inv_rows = list(csv.DictReader(open("/home/claude/work/complete_learning_inventory_revised.csv", encoding="utf-8-sig")))
inv_t = collections.Counter(norm(r["title"]) for r in inv_rows)
new_t = collections.Counter(norm(r["title"]) for r in rows)
missing = sorted(t for t in new_t if t not in inv_t)
print("\nnotebook titles absent from the inventory (normalized):", len(missing))
print("; ".join(missing))
print("\nin both, but more notebook sittings than inventory rows:")
for t, c in sorted(new_t.items()):
    if t in inv_t and c > inv_t[t]: print(f"  {t}: notebook {c} vs inventory {inv_t[t]}")
