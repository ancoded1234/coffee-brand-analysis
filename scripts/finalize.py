"""Validate analysis invariants, scan deliverables for the existing secret, package submission."""
from pathlib import Path
import json,zipfile,hashlib
import pandas as pd
import pymupdf as fitz
from dotenv import dotenv_values
from pptx import Presentation
R=Path(__file__).resolve().parents[1];P=R/'presentation';Q=R/'analysis/qa'
beans=pd.read_csv(R/'data/brand_beans.csv');prices=pd.read_csv(R/'data/price_observations.csv');comp=pd.read_csv(R/'data/comparison.csv');sources=pd.read_csv(R/'data/sources.csv')
assert len(beans)==len(comp)==6 and beans['브랜드명'].is_unique
assert len(prices)==8 and prices['관측ID'].is_unique
assert prices[prices['분석포함']]['HOT_ICE'].eq('HOT').all()
assert prices['샷수'].isna().all() and prices['원두투입량_g'].isna().all()
assert beans.loc[beans['브랜드명']=='파스쿠찌','아라비카비율'].isna().all()
assert beans.loc[beans['브랜드명']=='텐퍼센트커피','아라비카비율'].isna().all()
assert int(comp['아라비카비율'].notna().sum())==1
assert comp['기본가격'].max()-comp['기본가격'].min()==3200
assert comp.iloc[3:]['기본가격'].mean()==1900
assert comp.loc[comp['용량_mL'].isna(),'100mL당가격'].isna().all()
assert len(sources)==32
assert set(comp['브랜드명'])=={'스타벅스','투썸플레이스','폴 바셋','빽다방','텐퍼센트커피','컴포즈커피'}
assert comp.loc[comp['브랜드명']=='폴 바셋','용량_mL'].iloc[0]==360
for url in sources['출처URL']:assert url.startswith('https://')
doc=fitz.open(P/'coffee_brand_analysis.pdf');assert len(doc)==13
pdftext='\n'.join(p.get_text() for p in doc);normalized=''.join(pdftext.split());assert '비싼커피' in normalized and '3.13' in normalized
doc.close()
deck=Presentation(P/'coffee_brand_analysis.pptx');assert len(deck.slides)==13
assert all(sl.notes_slide.notes_text_frame.text.strip() for sl in deck.slides)
assert sum(sh.has_chart for sl in deck.slides for sh in sl.shapes)==2
office=json.loads((Q/'powerpoint_validation.json').read_text(encoding='utf-8'));assert all(c['success'] for c in office['native_chart_animation'])
browser=json.loads((Q/'browser_validation.json').read_text(encoding='utf-8'));assert not browser['errors'] and browser['video']['ready']>=2
videos=json.loads((Q/'video_validation.json').read_text(encoding='utf-8'));assert len(videos)==4 and all(v['frames']>100 for v in videos)
# File selection is explicit: no .env, virtual environment, browser profile or Manim cache.
files=[]
for f in R.rglob('*'):
    if not f.is_file():continue
    rel=f.relative_to(R);parts=set(rel.parts)
    if parts & {'.git','.venv','__pycache__','manim'} or f.name.startswith(('.env','~$')) or f.suffix=='.zip' or f.name in ['submission_manifest.json','final_validation.json']:continue
    if 'qa' in parts and f.suffix not in ['.json'] and f.name!='contact_sheet.jpg':continue
    if str(rel).startswith('data\\raw') and 'robots' not in parts:continue
    files.append(f)
secrets=[v for k,v in dotenv_values(R.parent/'.env').items() if v and ('KEY' in k or 'TOKEN' in k)]
hits=[]
for f in files:
    raw=f.read_bytes()
    if any(s.encode() in raw for s in secrets):hits.append(str(f.relative_to(R)))
    if f.suffix=='.pptx':
        with zipfile.ZipFile(f) as z:
            for n in z.namelist():
                raw=z.read(n)
                if any(s.encode() in raw for s in secrets):hits.append(f.name+':embedded file')
assert not hits,'Secret found in selected artifacts (content suppressed)'
report={'data_invariants':'passed','pdf_pages':13,'pptx_slides':13,'native_charts':2,'native_animation_effects':office['animation_effects'],'chart_wipes':len(office['native_chart_animation']),'manim_videos':videos,'source_count':len(sources),'secret_scan':'passed; values never printed','packaged_file_count':len(files),'public_deployment':'https://ancoded1234.github.io/coffee-brand-analysis/ (GitHub Pages)' if (R/'docs/index.html').exists() else 'local artifacts only'}
(Q/'final_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(Q/'final_validation.json')
manifest=[dict(path=f.relative_to(R).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files]
(R/'submission_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(R/'submission_manifest.json')
out=R/'coffee_brand_analysis_submission.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(f,Path('coffee-brand-analysis')/f.relative_to(R))
with zipfile.ZipFile(out) as z:
    assert len(z.namelist())==len(set(z.namelist()))
print(json.dumps({'checks':'passed','source_count':len(sources),'slides':13,'manim_videos':4,'submission_zip_MB':round(out.stat().st_size/1e6,2)},ensure_ascii=False,indent=2))
