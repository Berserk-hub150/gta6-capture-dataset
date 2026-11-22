import argparse, csv, hashlib, json, math, subprocess,tempfile
from pathlib import Path

def extract(clip,labels,out,fps):
    if out.exists(): raise ValueError('Choose a new output directory')
    if not math.isfinite(fps) or not 0<fps<=60: raise ValueError('fps must be in (0,60]')
    with labels.open(encoding='utf-8',newline='') as f:
        spans=sorted((float(r['start']),float(r['end']),r['label'].strip()) for r in csv.DictReader(f))
    for i,(a,b,name) in enumerate(spans):
        if not name or not math.isfinite(a+b) or not 0<=a<b or (i and a<spans[i-1][1]):
            raise ValueError('Expected labelled, finite, non-overlapping time intervals')
    with clip.open('rb') as f: source=hashlib.file_digest(f,'sha256').hexdigest()
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out.parent) as temp:
        batch=Path(temp)/'dataset';batch.mkdir();frames=batch/'frames';frames.mkdir()
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(clip),'-an','-vf',f'fps={fps}:start_time=0',
                        '-threads','1','-start_number','0',str(frames/'%07d.jpg')],check=True)
        files=sorted(frames.glob('*.jpg'))
        if not files: raise ValueError('No frames decoded')
        index=0
        with (batch/'manifest.jsonl').open('w',encoding='utf-8') as stream:
            for i,file in enumerate(files):
                t=i/fps
                while index<len(spans) and spans[index][1]<=t: index+=1
                label=spans[index][2] if index<len(spans) and t>=spans[index][0] else None
                row={'file':'frames/'+file.name,'seconds':t,'label':label,'clip_sha256':source}
                print(json.dumps(row),file=stream)
        batch.rename(out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('clip',type=Path);p.add_argument('labels',type=Path);p.add_argument('out',type=Path)
    p.add_argument('--fps',type=float,default=2);a=p.parse_args();extract(a.clip,a.labels,a.out,a.fps)
