"""Standalone HTML deck with locally vendored Anime.js; no runtime data fetch."""
from pathlib import Path
import json,html,shutil,requests
import pandas as pd
R=Path(__file__).resolve().parents[1];P=R/'presentation';A=P/'assets';e=html.escape
slides=json.loads((P/'slides.json').read_text(encoding='utf-8'));C=pd.read_csv(R/'data/comparison.csv').fillna('미공개');S=pd.read_csv(R/'data/sources.csv').fillna('미공개');metrics=json.loads((R/'analysis/metrics.json').read_text(encoding='utf-8'))
vendor=A/'anime.umd.min.js'
if not vendor.exists():
    r=requests.get('https://cdn.jsdelivr.net/npm/animejs@4.2.2/dist/bundles/anime.umd.min.js',timeout=30)
    if r.status_code!=200:r=requests.get('https://cdn.jsdelivr.net/npm/animejs@4.2.0/dist/bundles/anime.umd.min.js',timeout=30)
    r.raise_for_status();vendor.write_bytes(r.content)
    lic=requests.get('https://raw.githubusercontent.com/juliangarnier/anime/master/LICENSE.md',timeout=30)
    (A/'anime-LICENSE.txt').write_text(lic.text,encoding='utf-8')
def cards(items):return '<div class="cards">'+''.join(f'<article class="reveal"><small>{e(a)}</small><h3>{e(b)}</h3><p>{e(c)}</p></article>' for a,b,c in items)+'</div>'
def table(headers,rows):return '<div class="table"><div class="tr head">'+''.join(f'<span>{e(h)}</span>' for h in headers)+'</div>'+''.join('<div class="tr reveal">'+''.join(f'<span>{e(str(v))}</span>' for v in r)+'</div>' for r in rows)+'</div>'
def price_svg(group=False):
    rows=[('A 일반',4700),('B 가성비',1900)] if group else list(zip(C['브랜드명'],C['기본가격']))
    return '<svg class="price-chart" viewBox="0 0 900 410" role="img" aria-label="HOT 가격 공개 관측값 비교">'+''.join(f'<g class="price-row" tabindex="0" data-brand="{e(b)}"><title>{e(b)}: {v:,}원 | '+e('그룹 단순 평균' if group else str(C.iloc[i]['적용기준일'])+' | '+str(C.iloc[i]['매장위치']))+f'</title><text x="0" y="{45+i*(140 if group else 59)}" class="svg-label">{e(b)}</text><rect class="bar" x="185" y="{20+i*(140 if group else 59)}" width="{v/5600*560}" height="32" rx="4" fill="{("#754b36" if (i<3 if not group else i==0) else "#63765d")}"/><text class="svg-value" x="{200+v/5600*560}" y="{44+i*(140 if group else 59)}">{v:,}</text></g>' for i,(b,v) in enumerate(rows))+'<text class="axis-label" x="185" y="402">0</text><text class="axis-label" x="720" y="402">5,600원</text></svg>'
def species():
    return '<div class="species">'+''.join(f'<div class="recipe reveal"><b>{e(b)}</b><div class="recipe-track {"known" if i==0 else "unknown"}"><span>{"아라비카 100%" if i==0 else "비율 근거 미확보"}</span></div></div>' for i,b in enumerate(C['브랜드명']))+'</div>'
def claimsvg():
    out='<svg viewBox="0 0 920 380" class="claim-chart" role="img" aria-label="판매가격과 스페셜티 문구의 확인 상태">'
    for v in [1500,2500,3500,4700]:
        x=210+(v-1000)/4500*640;out+=f'<path d="M{x},45V310" stroke="#d7cbbb" stroke-dasharray="3 7"/><text x="{x}" y="350" text-anchor="middle" class="axis-label">{v:,}원</text>'
    out+='<text x="0" y="86" class="svg-label">주장 미확인</text><text x="0" y="257" class="svg-label">주장·보도 있음</text>'
    for i,r in C.iterrows():
        x=210+(r['기본가격']-1000)/4500*640;y=80 if i<3 else 250;dy=-26+i*42 if i<3 else -25 if i!=4 else 40
        out+=f'<g class="reveal"><title>{e(r["브랜드명"])} | {r["기본가격"]:,}원 | 품질 등급 아님</title><circle cx="{x}" cy="{y}" r="12" fill="{"#754b36" if i<3 else "#63765d"}"/><text x="{x-12 if i<3 else x}" y="{y+dy}" text-anchor="{"end" if i<3 else "middle"}" class="svg-label">{e(r["브랜드명"])}</text></g>'
    mobile='<div class="mobile-claims">'+''.join(f'<div class="reveal"><b>{e(r["브랜드명"])}</b><span>{r["기본가격"]:,}원</span><small>{"주장 미확인" if i<3 else "브랜드 주장" if i<5 else "외부 보도"}</small></div>' for i,r in C.iterrows())+'</div>'
    return out+'</svg>'+mobile
def specialty_bars():
    d=pd.read_csv(R/'data/specialty_components.csv')
    return '<div class="specialty-chart">'+''.join(f'<article class="reveal"><b>{e(r.브랜드명)}</b><div class="component-track"><div class="bar" style="width:{r.스페셜티구성분_pct}%"></div></div><p><strong>{r.스페셜티구성분_pct}%</strong> · {e(r.근거형태)}</p></article>' for r in d.itertuples())+'<p class="component-note">0–100% 동일 축. 다른 4개 브랜드는 함량 근거 미확보로 제외(0% 아님).<br>국가별 전체 배합비·아라비카 비율·맛 점수와 다르다.</p></div>'


def matrix():
    d=pd.read_csv(R/'data/disclosure_matrix.csv',index_col=0)
    return '<div class="disclosure">'+''.join('<div class="drow reveal"><b>'+e(str(idx))+'</b>'+''.join(f'<span class="{ "yes" if int(v) else "no" }" title="{e(col)}: {"공식 문구 확인" if int(v) else "이번 조사 미확인"}">{"확인" if int(v) else "미확인"}</span>' for col,v in row.items())+'</div>' for idx,row in d.iterrows())+'</div>'
bodies={
1:'<div class="cover-photo" role="img" aria-label="Google Flow가 생성한 커피 이미지"></div><div class="cover-copy"><small>THE PRICE OF A CUP</small><h1>비싼 커피는<br>정말 더 좋은<br>원두를 사용할까?</h1><p>한국 6대 카페 프랜차이즈의<br>원두 구성과 판매가격 데이터 분석</p><span class="edition">DATA LITERACY · 2026.10.18</span></div><span class="ai-credit">Google Flow AI 생성 이미지 · 분석 증거 아님</span>',
2:cards([('OBSERVE','판매가격','HOT 기본 아메리카노의 공개 가격'),('COMPARE','원두 특성','품종·산지·배전·인증을 각각 비교'),('TEST','품질의 증거','독립 점수와 관능평가 확보 여부')]),
3:'<div class="brand-groups">'+''.join('<article class="reveal"><small>'+grp+'</small>'+''.join('<h3>'+b+'</h3>' for b in names)+'</article>' for grp,names in [('A / 일반 프랜차이즈',['스타벅스','투썸플레이스','폴 바셋']),('B / 가성비 포지셔닝',['빽다방','텐퍼센트커피','컴포즈커피'])])+'</div>',
4:cards([('01 / FIND','공식 우선','공식 제품·원두·공정 자료'),('02 / COLLECT','Firecrawl','실제 본문·URL·수집시각 저장'),('03 / REVIEW','적용 범위 확인','온도·가격 기준일·제품 구분'),('04 / ANALYZE','8건 → HOT 6건','온도 미확인 2건은 비교 제외')])+'<div class="legend"><span>verified / 원문 확인</span><span>reported / 외부 보도</span><span>claimed / 자체 주장</span><span>unknown / 미확인</span></div>',
5:'<div class="split"><div>'+price_svg()+'</div><aside class="reveal"><strong class="big">3.13<span>×</span></strong><p>자료상 최고 / 최저</p><div class="stat">A 평균 <b>4,700원</b></div><div class="stat">B 평균 <b>1,900원</b></div><small>각 n=3 관측값의 단순 평균<br>전국 시장 평균 아님</small></aside></div><div class="fine">텐퍼센트: 울산비즈파크점 2,500원 · 스타벅스: Tall(최소 판매 Short와 다름) · 용량 확정 2/6 → 100mL 순위 보류</div>',
6:'<div class="split"><div>'+species()+'</div><aside class="reveal"><strong class="big">1<span>/6</span></strong><p>현재 비교 범위의<br>품종 비율 확인</p><h3>파스쿠찌 → 폴 바셋</h3><small>공식 생산국과 HOT 메뉴가<br>연결되는 유사 가격대 브랜드로<br>교체했다. 비율은 추정 안 함.</small></aside></div>',
7:table(['브랜드','산지 / 구성','로스팅','향미 문구'],[['스타벅스','지역 표기 충돌¹','다크','캐러멜·바디'],['투썸','블랙: 콜롬비아·브라질·PNG','다크 / 미디엄','초콜릿 / 과일·꽃'],['폴 바셋','브라질·에티오피아','국내 로스팅','초콜릿·산미·바디'],['빽다방','브라질: 벨로소 DOT·파젠다 엄³','5–15일 사용⁴','브라운슈가·견과'],['텐퍼센트','다크 4개국 / 미디엄 3개국','강배전 / 중배전²','초콜릿 / 과일'],['컴포즈','브라질·콜롬비아·에티오피아³','단계 미확인','고소함·초콜릿³']])+'<div class="fine">¹ 스타벅스 본문 라틴·아시아 / 하단 Origin 아프리카 → 국가 확정 보류　² 원문 ‘라이트 로스팅(중배전)’　³ 2026 취재·인터뷰　⁴ 로스팅 후 사용기간</div>',
8:table(['브랜드','확인한 내용','해석 범위'],[['스타벅스','C.A.F.E. Practices 안내','윤리 구매 ≠ 관능점수'],['투썸','HACCP·내부 Q-Grader','공정·관리 ≠ 독립 맛 평가'],['폴 바셋','스페셜티 선별·3–14일 사용','공식 관리 주장 ≠ 독립 평가'],['빽다방','파젠다 엄 스페셜티 20%','공식 배합 안내·평가표 미확보'],['텐퍼센트','상위 10% 스페셜티 주장','아라비카 함량 10% 아님'],['컴포즈','ス'.replace('ス','스')+'페셜티 5%·구성 원두 82점 보도','완성 블렌드 점수 아님']])+'<div class="bottom-stat"><b>0 / 6</b> 동일 기준으로 비교 가능한 독립 관능평가 점수 확보 건수</div>',
9:'<div class="split wide"><div>'+specialty_bars()+'</div><aside class="reveal"><h3>배합 함량<br>≠<br>품질 순위</h3><p>컴포즈 82점은 구성 원두 보도값. 완성 블렌드·매장 한 잔 점수가 아니다.</p></aside></div>',
10:cards([('01 / BEANS','원두','산지·생두·블렌딩·선별'),('02 / PROCESS','제조·관리','자체 플랜트·로스팅·품질 관리'),('03 / SPACE','공간·경험','좌석·디저트·매장 경험'),('04 / SERVICE','운영·서비스','추출·교육·주문 편의')])+'<div class="fine">공식 자료에서 확인한 제공 요소의 개념도. 면적·순서·개수는 비용 기여율을 의미하지 않는다.</div>',
11:'<div class="answer"><p class="reveal"><small>OBSERVED</small>자료상 HOT 가격은 1,500–4,700원</p><p class="reveal"><small>OBSERVED</small>가성비 그룹에도 스페셜티 사용 주장·보도</p><p class="reveal"><small>NOT ESTABLISHED</small>가격과 원두의 절대 품질·맛 사이의 관계</p></div>',
12:cards([('LIMITATION','조건 불일치','시점·매장·컵 크기 차이. 공급가·투입량·독립 평가 미확보.'),('MEASURE','동일 조건 구매','같은 날 HOT 기본 메뉴 구매. 영수증·실제 부피·온도 기록.'),('EXPERIMENT','익명 코드 시음','무작위 순서·동일 온도·반복 측정. 선호와 향미 평가 분리.')]),
13:'<div class="source-grid">'+''.join(f'<a href="{e(r.출처URL)}" target="_blank" rel="noopener" class="reveal"><small>{r.출처ID} / {e(r.신뢰등급)}</small><b>{e(r.브랜드명)} · {e(r.출처종류)}</b><span>{e(r.게시일)}</span></a>' for r in S.itertuples() if r.출처ID in ['S01','S02','S06','S13','S24','S25','S26','S27','S28','S29','S30','S31','S12','S17'])+'</div>'
}
# Build the production-country comparison from the audit, rather than abbreviating countries away.
origins=pd.read_csv(R/'data/origin_audit.csv')
profiles=[]
for i,r in C.iterrows():
    a=origins[origins['브랜드명']==r['브랜드명']].iloc[0]
    profiles.append([r['브랜드명'],a['생두생산국_지역'],a['농장_가공방식'],a['검증상태']])
bodies[7]=table(['브랜드','생두 생산국·지역','농장·가공방식','근거 상태'],profiles)+'<div class="fine">스타벅스는 공식 페이지 내부 지역 표기 충돌로 국가 구성 미확정. 빽다방 3종은 2026 현장 취재. 옵션별 전체 정보·URL·로스팅 장소는 origin_audit.csv.</div>'
sections=[]
for s in slides:
    n=s['number'];body=bodies[n]
    if n==1:markup=body
    else:markup=f'<small class="kicker">{e(s["kicker"])}</small><h2>{e(s["title"])}</h2><p class="subtitle">{e(s["subtitle"])}</p><div class="viz">{body}</div><footer>{e(s["source"] or "수집 2026.10.18 · 공개 자료 분석 · 품질 순위·인과관계 산출 안 함")}</footer>'
    sections.append(f'<section class="slide {"dark" if s["dark"] else ""} {"cover" if n==1 else ""}" aria-label="슬라이드 {n}" data-slide="{n}">{markup}<span class="folio">{n:02} / 13</span></section>')
page='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>비싼 커피는 정말 더 좋은 원두를 사용할까?</title><link rel="stylesheet" href="assets/deck.css"></head><body><header class="toolbar"><a class="wordmark" href="#1">COFFEE / EVIDENCE / VALUE</a><nav><button id="motion">모션 설명</button><button id="disclosure">공개 수준</button><button id="notes">발표 노트</button><button id="sources">출처</button><button id="fullscreen" aria-label="전체 화면">전체 화면 ↗</button></nav></header><main id="stage">'''+''.join(sections)+'''</main><div class="controls"><button id="prev" aria-label="이전 슬라이드">←</button><span id="page">01 / 13</span><div class="track"><div id="progress"></div></div><button id="replay" aria-label="그래프 다시 재생">↻</button><button id="next" aria-label="다음 슬라이드">→</button></div><dialog id="dialog"><button id="close" aria-label="닫기">닫기 ×</button><div id="dialog-content"></div></dialog><script src="assets/anime.umd.min.js"></script><script>const SLIDES='''+json.dumps(slides,ensure_ascii=False)+''';const SOURCES='''+json.dumps(S.to_dict('records'),ensure_ascii=False)+''';const DISCLOSURE='''+json.dumps(matrix(),ensure_ascii=False)+''';</script><script src="assets/deck.js"></script></body></html>'''
(P/'index.html').write_text(page,encoding='utf-8');print('HTML deck built; Anime.js vendored')
