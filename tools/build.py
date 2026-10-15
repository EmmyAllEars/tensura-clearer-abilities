"""Builds the pack's lang files: controls first, then Tensura's own description.
Inputs: data/controls.json (facts read from the mod jars), data/abilities_in_use.json (which abilities the family has),
the reference data (~/code/tensura-guide/work/data.json) and the mods' own lang files (for mode names and descriptions)."""
import json,os,sys
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG={'tensura':json.load(open(sys.argv[1])),'mysticism':json.load(open(sys.argv[2]))}
ref={a['id']:a for a in json.load(open(os.path.expanduser('~/code/tensura-guide/work/data.json')))['abilities']}
ctl=json.load(open(os.path.join(R,'data/controls.json')))
if os.path.exists(os.path.join(R,'data/controls_rest.json')): ctl.update(json.load(open(os.path.join(R,'data/controls_rest.json'))))
use=list(ref)  # every ability in Tensura and Mysticism; data/abilities_in_use.json records what the family had
H=json.load(open(os.path.join(R,'data/handwritten.json')))
AW=os.path.join(R,'data/agent_written.json')
if os.path.exists(AW): H={**json.load(open(AW)),**H}  # handwritten wins
E='§e';G='§6';B='§b';X='§r'
SNEAK={
 'tensura:analytical_appraisal':f'{E}Sneak + press{X}: switch what it analyses (entities, blocks or both).',
 'tensura:gravity_field':f'{E}Sneak + press{X}: cancel the field.',
 'tensura:thought_communication':f'{E}Sneak{X} while ordering: give the order to all nearby subordinates.',
 'tensura:blizzard':f'{E}Sneak + press{X}: dismiss your blizzard.',
}
SCROLL={'power':f'{E}Scroll{X} (mastered): Power Scale, how much of your EP it uses.','range':f'{E}Scroll{X}: change range.'}
SCROLLKIND={'tensura:haki':'power','tensura:demon_lord_haki':'power','tensura:coercion':'power','tensura:mortal_fear':'power',
            'tensura:molecular_manipulation':'range','tensura:farsight':'range'}
HOW={'Cast':f'{E}Hold{X} to cast, then release.','Press key':f'{E}Press{X} to use.','Hold key':f'{E}Hold{X} to use.',
     'Press or hold':f'{E}Press{X} to use; some effects need it {E}held{X}.'}
def mode_names(sid,c):
    ns=sid.split(':')[0]; L=LANG[ns]
    names=[L.get(f'{ns}.skill.mode.{m}') for m in c.get('modeids',[])]
    names=[n for n in names if n]
    n=c.get('modes')
    if isinstance(n,int) and len(names)<n:
        names=ref[sid]['modes'] or names
    return names
out={'tensura':{},'mysticism':{}}; skipped=[]
for sid in use:
    ns,name=sid.split(':'); key=f'{ns}.skill.{name}.description'
    if key in H: out[ns][key]=H[key]; continue
    a=ref.get(sid); c=ctl.get(sid,{})
    orig=LANG[ns].get(key)
    passive = a is not None and a['use'] in ('Passive','Always on')
    if not a or not orig or a['use']=='Unknown' or (not passive and not c.get('class')): skipped.append(sid); continue
    lines=[]
    if a['use'] in ('Passive','Always on'):
        lines.append(f'{B}Passive{X}: always on.')
    else:
        how=HOW.get(a['how'] or '', f'{E}Press{X} to use.')
        if a['use']=='Passive and active':
            if a['tog']=='always':
                lines.append(f'{B}Passive{X} while toggled on; {E}press{X} to toggle.')
            elif a['tog']=='mastered':
                lines.append(f'{B}Passive{X} effect. '+how.replace(' to use.',' to use it actively;')+' toggles once mastered.')
            else:
                lines.append(f'{B}Passive{X} effect. '+how)
        else:
            lines.append(how)
        m=mode_names(sid,c)
        if len(m)>1: lines.append(f'{G}Modes{X}: '+', '.join(m)+'.')
        if sid in SNEAK: lines.append(SNEAK[sid])
        if sid in SCROLLKIND: lines.append(SCROLL[SCROLLKIND[sid]])
    out[ns][key]='\n'.join(lines)+'\n§7'+orig
for ns,d in out.items():
    p=os.path.join(R,'pack/assets',ns,'lang/en_us.json'); os.makedirs(os.path.dirname(p),exist_ok=True)
    json.dump(dict(sorted(d.items())),open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('written',sum(len(d) for d in out.values()),'skipped',skipped)
