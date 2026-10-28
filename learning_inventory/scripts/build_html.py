import json
d = json.load(open("/home/claude/work/data.json", encoding="utf-8"))
s = open("/home/claude/work/template.html", encoding="utf-8").read()
payload = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
open("/home/claude/work/conceptual_network.html", "w", encoding="utf-8").write(s.replace("__DATA__", payload))
print(len(s), len(payload))
