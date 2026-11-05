import re,glob,sys
files=sorted(glob.glob('src/[0-9][0-9]_*.tex'))
txt='\n'.join(open(f).read() for f in files)
# bibliography file (may not exist yet)
try: bib=open('src/bib.tex').read()
except: bib='\\begin{thebibliography}{99}\\bibitem{mancinelli2006} M. Mancinelli. \\bibitem{abate2012} A. Abate.\\end{thebibliography}'
def conv(m):
    body=m.group(2)
    lab=m.group(1) or ''
    items=[i.strip() for i in re.split(r'\\item\s*',body) if i.strip()]
    if 'roman' in lab: names=['(i)','(ii)','(iii)','(iv)','(v)','(vi)','(vii)','(viii)']
    elif 'alph' in lab: names=['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)']
    else: names=['(%d)'%(k+1) for k in range(len(items))]
    out=[]
    for n,i in zip(names,items):
        i=i.rstrip(';. ')
        out.append(n+' '+i)
    return '; '.join(out)+'.'
txt=re.sub(r'\\begin\{enumerate\}(?:\[label=([^\]]*)\])?(.*?)\\end\{enumerate\}',conv,txt,flags=re.S)
CLS={'prop:stepvalidity':'structural','prop:auditcontext':'impossibility or independence','prop:reorg': 'definitional consequence', 'prop:idemp': 'definitional consequence', 'prop:ops': 'definitional consequence', 'prop:forknoconstrain': 'definitional consequence', 'prop:resp': 'definitional consequence', 'prop:coverage': 'definitional consequence', 'prop:succession': 'definitional consequence', 'prop:sovereignty': 'definitional consequence', 'thm:portability': 'definitional consequence', 'prop:compose': 'definitional consequence', 'prop:noreorder': 'definitional consequence', 'prop:independence': 'structural', 'prop:suffstructure': 'structural', 'prop:restime': 'structural', 'prop:envtradeoff': 'structural', 'prop:noise': 'structural', 'prop:slot': 'structural', 'prop:atomic': 'structural', 'thm:merkle': 'structural', 'prop:incompat': 'structural', 'prop:debtprops': 'structural', 'prop:orphanroutes': 'structural', 'prop:mergebase': 'structural', 'thm:pathmerge': 'structural', 'thm:closure': 'structural', 'prop:expansion': 'structural', 'prop:grounded': 'structural', 'prop:minarch': 'structural', 'prop:replace': 'structural', 'prop:reuse': 'impossibility or independence', 'prop:classlimit': 'impossibility or independence', 'prop:contract': 'impossibility or independence', 'prop:intent': 'impossibility or independence', 'prop:compile': 'impossibility or independence', 'prop:namesidentify': 'impossibility or independence', 'prop:semver': 'impossibility or independence', 'prop:unauth': 'impossibility or independence', 'prop:count': 'impossibility or independence', 'prop:techlegal': 'impossibility or independence', 'prop:attribution': 'impossibility or independence', 'prop:refusal': 'impossibility or independence', 'prop:devindep': 'impossibility or independence', 'prop:nototal': 'impossibility or independence', 'prop:projloss': 'impossibility or independence', 'prop:squash': 'impossibility or independence', 'thm:symmetry': 'impossibility or independence', 'cor:nonunique': 'impossibility or independence', 'thm:fourindep': 'impossibility or independence', 'prop:gap': 'impossibility or independence', 'prop:iav': 'impossibility or independence', 'prop:timestamp': 'impossibility or independence', 'prop:verinf': 'impossibility or independence', 'prop:tests': 'impossibility or independence', 'prop:disclosure': 'impossibility or independence', 'prop:moves': 'impossibility or independence', 'prop:cochange': 'impossibility or independence', 'prop:embed': 'impossibility or independence', 'prop:ruleversion': 'impossibility or independence', 'prop:nontransfer': 'impossibility or independence', 'prop:funclegit': 'impossibility or independence', 'prop:size': 'impossibility or independence', 'prop:nphard': 'complexity', 'thm:installability': 'complexity', 'prop:extpreserve': 'preservation', 'thm:lineageinv': 'preservation', 'thm:lineagepres': 'preservation', 'thm:extraction': 'preservation', 'thm:hoisting': 'preservation', 'thm:revision': 'preservation', 'thm:interface': 'preservation', 'prop:twochannel': 'model-dependent quantitative', 'prop:increase': 'model-dependent quantitative', 'prop:axis': 'model-dependent quantitative', 'prop:labelcap': 'model-dependent quantitative', 'cor:reconstruct': 'model-dependent quantitative', 'prop:convention': 'model-dependent quantitative', 'prop:ordering': 'model-dependent quantitative', 'prop:polya': 'model-dependent quantitative', 'prop:overload': 'model-dependent quantitative', 'prop:nocycle': 'model-dependent quantitative', 'prop:dominance': 'model-dependent quantitative', 'prop:lockin': 'model-dependent quantitative', 'prop:quorum': 'model-dependent quantitative', 'thm:anchor': 'model-dependent quantitative', 'prop:chain': 'model-dependent quantitative', 'prop:replication': 'model-dependent quantitative', 'prop:threshold': 'model-dependent quantitative', 'prop:critmass': 'model-dependent quantitative', 'cor:interop': 'model-dependent quantitative', 'prop:corrsupport': 'model-dependent quantitative', 'conj:fedscale': 'conjecture', 'conj:lattice': 'conjecture'}
envs='theorem|proposition|lemma|corollary|conjecture'
rows=[]
for m in re.finditer(r'\\begin\{(%s)\}(\[([^\]]*)\])?(\\label\{([^}]*)\})?(.*?)\\end\{\1\}'%envs,txt,flags=re.S):
    kind,title,lab,body=m.group(1),m.group(3) or '',m.group(5),m.group(6)
    st=re.search(r'\\(Proved|Tested|Conj|Design)\b',body)
    st=st.group(1) if st else None
    pidx=len(re.findall(r'\\part\{',txt[:m.start()]))
    if lab: rows.append((kind,title,lab,st,pidx))
    if lab not in CLS: print('UNCLASSIFIED',lab)
names={'Proved':'proved','Tested':'investigated','Conj':'conjectural','Design':'design argument',None:'unlabeled'}
reg='\\chapter{Register of Results by Epistemic Status}\\label{app:register}\n\nThis register is generated from the source of the book. Each entry gives the kind, number, title, and the status label attached to the statement. The label records the kind of support and not its strength: a result proved for a toy model, a result proved under a cryptographic idealization, and a result that is a direct consequence of a definition all carry the same label, and the qualification stated with each result should be read together with the register.\n\n'
for key in ['Proved','Tested','Conj','Design',None]:
    sel=[r for r in rows if r[3]==key]
    if not sel: continue
    reg+='\\section*{%s (%d)}\n\\begin{longtable}{p{0.11\\textwidth}p{0.10\\textwidth}p{0.42\\textwidth}p{0.23\\textwidth}}\n\\toprule\nKind & No. & Title & Class \\\\\n\\midrule\n\\endhead\n'%(names[key],len(sel))
    for kind,title,lab,_,_p in sel:
        reg+='%s & \\Cref{%s} & %s & %s \\\\\n'%(kind.capitalize(),lab,title,CLS.get(lab,'unclassified'))
    reg+='\\bottomrule\n\\end{longtable}\n\n'
rom=['','I','II','III','IV','V','VI','VII','VIII','IX']
cnt={}
for r in rows:
    cnt.setdefault(r[4],{}).setdefault(r[3],0)
    cnt[r[4]][r[3]]+=1
tb='\\section*{Counts by part}\n\\begin{tabular}{lrrrr}\n\\toprule\nPart & Proved & Investigated & Conjectural & Design \\\\\n\\midrule\n'
for k in sorted(cnt):
    c=cnt[k]
    tb+='%s & %d & %d & %d & %d \\\\\n'%(rom[k] if k<len(rom) else str(k),c.get('Proved',0),c.get('Tested',0),c.get('Conj',0),c.get('Design',0))
tb+='\\bottomrule\n\\end{tabular}\n\n'
cc={}
for r in rows: cc[CLS.get(r[2],'unclassified')]=cc.get(CLS.get(r[2],'unclassified'),0)+1
tc='\\section*{Counts by mathematical function}\nThe class describes what kind of statement a result is and not how important it is. Definitional consequences follow from definitions in a few lines; structural results establish properties or equivalences of the defined objects; impossibility or independence results exhibit constructions showing that something cannot be derived or that properties are independent; complexity results concern computational hardness; preservation results state which invariants survive a transformation; model-dependent quantitative results are exact for a stipulated model or idealization.\n\n\\begin{tabular}{lr}\n\\toprule\nClass & Results \\\\\n\\midrule\n'
for k in sorted(cc): tc+='%s & %d \\\\\n'%(k,cc[k])
tc+='\\bottomrule\n\\end{tabular}\n\n'
tb=tb+tc
reg=reg.replace('\\section*{proved',tb+'\\section*{proved',1)
txt+='\n'+reg
txt+='\n\\backmatter\n'
txt+=bib
txt+='\n\\end{document}\n'
open('architecture_of_continuity.tex','w').write(txt)
