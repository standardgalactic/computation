import csv, collections

PS = "Psychology and Cognitive Science"; BI = "Biology, Neuroscience and Health"
AR = "Arts, Music and Literature"; LA = "Languages and Linguistics"
PL = "Philosophy, Logic and Critical Thinking"; SO = "Social Sciences and Economics"
HI = "History"; MA = "Mathematics and Statistics"; PH = "Physics and Astronomy"
CH = "Chemistry and Materials"; ES = "Earth and Environmental Science"
EN = "Engineering and Applied Technology"; ED = "Education and Pedagogy"
GS = "General Science and Interdisciplinary"
N = ""

# title, lecturer, date (2016), circled number, format, notes, primary, secondary
R = [
 ("Big History", "David Christian", "Jan 4", "48", "Lecture series", "", HI, PH),
 ("Brief History", "Peter N. Stearns", "Jan 5", "36", "Lecture series", "", HI, N),
 ("Building Great Sentences", "Brooks Landon", "Jan 6", "24", "Lecture series", "", LA, AR),
 ("Cosmology", "Mark Whittle", "Jan 7", "36", "Lecture series", "Title underlined in notebook", PH, N),
 ("Archeology", "Susan Foster McCarter", "Jan 8", "24", "Lecture series", "", HI, SO),
 ("Existentialism", "Robert C. Solomon", "Jan 8", "24", "Lecture series", "Initial written as E; read as C", PL, N),
 ("Human Anatomy", "John K. Young", "Jan 9", "14", "Lecture series", "Marked with an asterisk", BI, N),
 ("Music & Math", "David Kung", "Jan 9", "12", "Lecture series", "", MA, AR),
 ("Infectious Diseases", "Barry C. Fox", "Jan 10", "24", "Lecture series", "", BI, N),
 ("Nanotechnology", "Shana Kelley, Ted Sargent", "Jan 11", "24", "Lecture series", "", EN, CH),
 ("Physics of History", "David J. Helfand", "Jan 12", "24", "Lecture series", "", GS, HI),
 ("Superstring Theory", "S. James Gates Jr.", "Jan 12", "24", "Lecture series", "", PH, N),
 ("Astronomy, Stars, Galaxies...", "James Kaler", "Jan 12", "13", "Lecture series", "Lecture count of 13 confirmed by the user", PH, N),
 ("Effective Communication Skills", "Dalton Kehoe", "Jan 13", "24", "Lecture series", "", LA, PS),
 ("How Conversation Works", "Anne Curzan", "Jan 13", "6", "Lecture series", "", LA, PS),
 ("Memory and the Human Lifespan", "Steve Joordens", "Jan 14", "24", "Lecture series", "", PS, N),
 ("Analysis & Critique", "Dorsey Armstrong", "", "24", "Lecture series", "Date not visible; marked (LT)", PL, LA),
 ("Cognitive Behavioral Therapy: Techniques for Retraining Your Brain", "Jason M. Satterfield", "", "24", "Lecture series", "Date not visible", PS, N),
 ("Consciousness and Its Implications", "Daniel N. Robinson", "Jan 16", "12", "Lecture series", "", PL, PS),
 ("Fundamentals of Sustainable Living", "Lonnie A. Gamble", "Jan 16", "12", "Lecture series", "Title partly legible", ES, N),
 ("From Plato to Postmodernism: The Role of the Author", "Louis Markos", "Jan 17", "24", "Lecture series", "Marked (LT); circled number uncertain", AR, PL),
 ("The History of Science from Antiquity to 1700", "Lawrence M. Principe", "", "36", "Lecture series", "Date not visible", HI, N),
 ("The History of Science 1700-1900", "Frederick Gregory", "Jan 19", "36", "Lecture series", "", HI, N),
 ("Money and Banking", "Michael K. Salemi", "Jan 21", "36", "Lecture series", "", SO, N),
 ("Being Human", "Robert Sapolsky", "Jan 21", "12", "Lecture series", "", BI, N),
 ("Classical Mythology", "Elizabeth Vandiver", "Jan 22", "19", "Lecture series", "Notebook count of 19 confirmed by the user; the publisher lists 24, but the user only had 19 lectures (the quadrivium transcriptions also hold 19)", HI, N),
 ("Doctors: History of Medicine", "Sherwin B. Nuland", "Jan 22", "12", "Lecture series", "", HI, BI),
 ("Great Ideas of Classical Physics", "Steven Pollock", "Jan 23", "24", "Lecture series", "", PH, N),
 ("The African Experience", "Kenneth P. Vickery", "Jan 24", "36", "Lecture series", "", HI, N),
 ("Ancient Greek Civilization", "Jeremy McInerney", "Jan 25", "24", "Lecture series", "", HI, N),
 ("Biological Anthropology", "Barbara J. King", "Jan 25", "24", "Lecture series", "Lecture count of 24 confirmed by the user and by the 24 numbered lecture files in the quadrivium folder", BI, SO),
 ("Biology and Human Behavior", "Robert Sapolsky", "Jan 26", "24", "Lecture series", "", BI, PS),
 ("Change and Motion", "Michael Starbird", "Jan 27", "24", "Lecture series", "", MA, N),
 ("Foundations of Western Civilization", "Thomas F. X. Noble", "Jan 29", "48", "Lecture series", "", HI, N),
 ("Foundations of Western Civilization II", "Robert Bucholz", "Jan 31", "48", "Lecture series", "", HI, N),
 ("Great Ideas of Philosophy", "Daniel Robinson", "Feb 2", "50", "Lecture series", "Boxed note: 46.5 hrs", PL, N),
 ("Great Ideas of Psychology", "Daniel Robinson", "Feb 4", "48", "Lecture series", "Title partly illegible; note: 1978, 48 hrs", PS, N),
 ("The Joy of Thinking", "Ed Burger, Mike Starbird", "Feb 5", "24", "Lecture series", "", PL, MA),
 ("Natural Law and Human Nature", "Joseph Koterski", "Feb 5", "24", "Lecture series", "", PL, N),
 ("Passions: Philosophy and the Intelligence of Emotions", "Robert C. Solomon", "Feb 6", "24", "Lecture series", "", PL, PS),
 ("Conflict Management", "Michael Dues", "Feb 7", "24", "Lecture series", "Lecture count of 24 confirmed by the user and by the 24 numbered lecture files in the quadrivium folder", SO, PS),
 ("Inexplicable Universe", "Neil deGrasse Tyson", "Feb 7", "6", "Lecture series", "", PH, N),
 ("Impossible: Physics Beyond the Edge", "Benjamin Schumacher", "Feb 8", "24", "Lecture series", "Written over a crossed-out Physics of the Impossible", PH, N),
 ("Rise of Humans: Great Scientific Debates", "John Hawks", "Feb 9", "24", "Lecture series", "", BI, N),
 ("Quantum Mechanics", "Benjamin Schumacher", "Feb 10", "24", "Lecture series", "", PH, N),
 ("Quantum: Einstein, Bohr, and the Great Debate", "Manjit Kumar", "Feb 11", "", "Audiobook", "15 chapters", PH, N),
 ("Science in the Twentieth Century", "Steven Goldman", "Feb 12", "36", "Lecture series", "", HI, N),
 ("The Nature of Matter", "David W. Ball", "Feb 13", "24", "Lecture series", "", CH, PH),
 ("Amazing Quantum", "James Kakalios", "Feb 14", "", "Audiobook", "21 chapters; marked (AB)", PH, N),
 ("Game Theory", "Scott P. Stevens", "Feb 15", "24", "Lecture series", "", MA, SO),
 ("How Ideas Spread", "Jonah Berger", "Feb 15", "12", "Lecture series", "", SO, PS),
 ("Meteorology", "Robert G. Fovell", "Feb 16", "24", "Lecture series", "", ES, N),
 ("How the Earth Works", "Michael E. Wysession", "Feb 17", "18", "Lecture series", "", ES, N),
 ("High School Math", "", "Feb 18", "30", "Lecture series", "Lecturer line left blank", MA, N),
 ("How to Become a Super Star Student", "", "", "", "Lecture series", "Crossed out in notebook", ED, N),
 ("Geometry", "", "Feb 19", "", "Lecture series", "", MA, N),
 ("Studying", "", "Feb 20", "", "Lecture series", "Circled number unreadable", ED, N),
 ("Rhetoric, Poetics, Logic", "Aristotle", "Feb 22", "", "Reading", "Numbered alpha in margin", PL, AR),
 ("Buddhism", "", "Feb 23", "", "Unspecified", "Numbered beta in margin", PL, N),
 ("God", "", "Feb 23", "", "Unspecified", "Numbered gamma in margin", PL, N),
 ("Modern Mind", "Alan Charles Kors", "Feb 24", "", "Lecture series", "", HI, PL),
 ("Argumentation", "", "Feb 25", "", "Lecture series", "Margin note: 15 x 4 = 60", PL, N),
 ("New Testament", "", "Feb 26", "", "Unspecified", "Date partly legible", HI, N),
 ("C. S. Lewis", "", "Feb 26", "", "Unspecified", "", AR, PL),
 ("The Long 19th Century: European History from 1789 to 1917", "Robert I. Weiner", "Feb 27", "36", "Lecture series", "Struck through in notebook, but the user confirms the course was completed; Great Courses course no. 8190, 36 lectures; separate course from Brief History", HI, N),
 ("Psychology of Behaviour", "", "Feb 28", "", "Lecture series", "Written over a crossed-out Behavioural Psychology", PS, N),
 ("Geology: Origin and Evolution of Earth", "Robert M. Hazen", "Mar 2", "", "Lecture series", "", ES, N),
 ("Negotiation: Getting the Best Deal", "", "Mar 4", "", "Lecture series", "", SO, PS),
 ("Planets and the Sun", "", "Mar 5", "", "Lecture series", "", PH, N),
 ("Quest for Meaning", "", "Mar 6", "", "Lecture series", "Note: missing 5 lectures", PL, N),
 ("The Search for Intelligent Life in Space", "", "Mar 7", "", "Lecture series", "Boxed note: break with outline", PH, BI),
 ("Modern Physics", "", "Mar 8", "", "Lecture series", "", PH, N),
 ("Everyday Physics", "", "Mar 9", "", "Lecture series", "Date partly legible; written in blue", PH, N),
 ("Domestication", "", "Mar 10", "", "Lecture series", "", BI, HI),
 ("Courtroom Cases", "", "Mar 11", "", "Lecture series", "", SO, N),
 ("Abiogenesis", "", "Mar 13", "", "Lecture series", "", BI, CH),
 ("Mental Math", "", "Mar 14", "", "Lecture series", "", MA, N),
 ("Reality", "", "Mar 15", "", "Lecture series", "Date written as Mar 16, same as the next entry", PL, N),
 ("Angelic Doctor: Thomas Aquinas", "", "Mar 16", "", "Lecture series", "", PL, N),
 ("Entanglement", "Louisa Gilder", "Mar 18", "", "Audiobook", "", PH, N),
 ("Scientific Ideas That Changed the World", "Stephen L. Goldman", "Mar 20", "", "Lecture series", "", GS, HI),
]

LISTED = {'Classical Mythology': '24', 'Brief History': '36', 'The Long 19th Century: European History from 1789 to 1917': '36'}
AMBIG = {"Conflict Management", "Negotiation: Getting the Best Deal", "Courtroom Cases", "Reality", "Buddhism", "God",
         "New Testament", "Quest for Meaning", "Domestication", "Brief History"}
rows = []
for i, (t, who, d, n, fmt, note, p, q) in enumerate(R, 1):
    basis = "Title and lecturer based"
    if t in AMBIG or "uncertain" in note or "unclear" in note or "illegible" in note or "obscured" in note:
        basis += "; ambiguous or uncertain"
    rows.append({
        "entry_id": f"N16-{i:03d}", "source": "Handwritten lecture notebook", "sequence_in_batch": i,
        "title": t, "lecturer": who, "date_text": d, "year": "2016", "period": "Notebook 2016 (Jan to Mar pages)",
        "format": fmt, "lectures_recorded": n, "lectures_listed": LISTED.get(t, ""), "notes": note,
        "revised_primary_discipline": p, "revised_secondary_discipline": q, "classification_basis": basis})

with open("/home/claude/work/notebook_2016_early_pages.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print(len(rows), "rows")
for k, v in collections.Counter(r["revised_primary_discipline"] for r in rows).most_common(): print(v, k)
print("dated:", sum(1 for r in rows if r["date_text"]), "with circled count:", sum(1 for r in rows if r["lectures_recorded"]),
      "audiobooks:", sum(1 for r in rows if r["format"] == "Audiobook"))
inv = {r["title"].lower() for r in csv.DictReader(open("/home/claude/work/complete_learning_inventory_revised.csv", encoding="utf-8-sig"))}
print("titles also in existing inventory:", sorted(t for t, *_ in R if t.lower() in inv))
