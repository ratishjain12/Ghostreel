import json,subprocess
Wd=json.load(open('audio/script-words.json'))
W=json.load(open('audio/whisper-words.json'))
TOTAL=61.217375
starts=["First,","Second,","Third,","Fourth,","Fifth,","Sixth,","And","CPU,","Comment"]
idx=[0]; k=0
for s in starts:
    k=next(i for i in range(k+1,len(Wd)) if Wd[i]['text']==s); idx.append(k)
idx.append(len(Wd))
bounds=[0.0]
for i in idx[1:-1]:
    bounds.append(round((Wd[i-1]['end']+Wd[i]['start'])/2,3))
bounds.append(TOTAL)
voices=[]
subprocess.run("mkdir -p audio/frame-clips",shell=True)
for f in range(10):
    a,b=bounds[f],bounds[f+1]; p=f"audio/frame-clips/{f+1:02d}.wav"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i","audio/linux-commands-for-a-broken-prod-box.wav","-ss",str(a),"-to",str(b),"-c:a","pcm_s16le",p],check=True)
    words=[{"id":f"w-{f+1:02d}-{j}","text":w['text'],"start":round(max(0,w['start']-a),3),"end":round(min(b,w['end'])-a,3)} for j,w in enumerate(Wd[idx[f]:idx[f+1]])]
    voices.append({"frame":f+1,"path":p,"duration_s":round(b-a,3),"words":words})
    print(f+1,a,b,round(b-a,3),' '.join(w['text'] for w in words))
json.dump({"bgm":None,"bgm_pending":False,"voices":voices,"sfx":[]},open('audio_meta.json','w'),indent=2)
