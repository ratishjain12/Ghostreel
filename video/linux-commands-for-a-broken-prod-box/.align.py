import json,re,difflib
W=json.load(open('audio/whisper-words.json'))
script=open('user_script.txt').read().split()
norm=lambda s:re.sub(r"[^a-z0-9]","",s.lower())
a=[norm(x['w']) for x in W]; b=[norm(x) for x in script]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
T=[None]*len(script)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1): T[j1+k]=(W[i1+k]['s'],W[i1+k]['e'])
    elif tag=='replace' and i2>i1:
        s,e=W[i1]['s'],W[i2-1]['e']; n=j2-j1
        for k in range(n): T[j1+k]=(round(s+(e-s)*k/n,3),round(s+(e-s)*(k+1)/n,3))
# fill gaps (insertions) by interpolating between neighbors
for j in range(len(T)):
    if T[j] is None:
        p=next((T[k][1] for k in range(j-1,-1,-1) if T[k]),0)
        q=next((T[k][0] for k in range(j+1,len(T)) if T[k]),p+0.3)
        T[j]=(p,max(p+0.05,min(q,p+0.3)))
out=[{"text":script[j],"start":T[j][0],"end":T[j][1]} for j in range(len(script))]
json.dump(out,open('audio/script-words.json','w'),indent=0)
print(' '.join(f"{o['text']}[{o['start']}]" for o in out))
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag!='equal': print(tag,[x['w'] for x in W[i1:i2]],script[j1:j2])
