"""Merges agent-written batches (markup: *control*, [Mode], {P}) into data/agent_written.json as colour-coded text.
Usage: python3 tools/merge_agent.py <dir with batchNN.json files>"""
import json,os,re,sys,glob
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def fmt(s):
    s=re.sub(r'\*([^*\n]+)\*',r'§e\1§r',s)
    s=re.sub(r'\[([^\]\n]+)\]',r'§6\1§r',s)
    return s.replace('{P}','§bPassive§r')
p=os.path.join(R,'data/agent_written.json')
out=json.load(open(p)) if os.path.exists(p) else {}
skipped=[]
for f in sorted(glob.glob(os.path.join(sys.argv[1],'batch*.json'))):
    try: d=json.load(open(f,encoding='utf-8'))
    except Exception as e: print('BAD JSON',f,e); continue
    for k,v in d.items():
        if not isinstance(v,str) or v.startswith('SKIP'): skipped.append(k); continue
        out[k]=fmt(v)
json.dump(dict(sorted(out.items())),open(p,'w'),ensure_ascii=False,indent=2)
print('agent-written total',len(out),'skipped',skipped)
