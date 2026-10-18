"""Manually reviewed public evidence -> reproducible CSVs. No inferred recipes or quality ranks."""
from pathlib import Path
import json,datetime
import pandas as pd
R=Path(__file__).resolve().parents[1]
DATE='2026-10-18'
U='이번 조사에서 미확보'
SPECS=[
('S01','스타벅스','starbucks_arabica','공식 홈페이지','게시일 미표기','아라비카만 구매; 선별·로스팅 방식 안내','verified'),
('S02','스타벅스','starbucks_espresso_verified','공식 제품 자료','게시일 미표기','에스프레소 로스트; 다크·캐러멜; 본문과 Origin 항목의 지역 표기가 충돌','verified'),
('S03','스타벅스','starbucks_ethics','공식 홈페이지','게시일 미표기','C.A.F.E. Practices 윤리 구매 검증 설명; SCA 관능점수와 다른 지표','verified'),
('S04','스타벅스','starbucks_price','언론(뉴시스)','2025-01-20','2025-01-24부터 톨 아메리카노 4,700원','reported'),
('S05','스타벅스','starbucks_hot_verified','공식 메뉴','게시일 미표기','HOT 카페 아메리카노 Tall 355mL','verified'),
('S06','투썸플레이스','twosome_beans','공식 홈페이지','게시일 미표기','블랙그라운드: 콜롬비아·브라질·파푸아뉴기니, 다크; 아로마노트: 에티오피아·과테말라, 미디엄','verified'),
('S07','투썸플레이스','twosome_roast','공식 홈페이지','게시일 미표기','자체 플랜트·색상 선별·내부 Q-Grader·HACCP 안내; 제품별 독립 관능점수는 확인 못함','verified'),
('S08','투썸플레이스','twosome_price','언론(한국경제)','2025-03-24','2025-03-26부터 레귤러 아메리카노 4,700원','reported'),
('S09','파스쿠찌','pascucci_beans','공식 홈페이지','게시일 미표기','가문 전통 블렌드 80:20 설명과 골든색 설명이 별도; 현재 한국 매장용 배합비의 명시적 연결 없음','verified'),
('S10','파스쿠찌','pascucci_price','언론(이투데이)','2025-02-12','2025-02-13부터 레귤러 아메리카노 4,700원','reported'),
('S11','빽다방','paik_beans','공식 홈페이지','게시일 미표기','파젠다 엄 스페셜티 원두 활용 블렌딩, 브라질, 뉴크롭·DOT 설명; 실제 로트 점수 미공개','claimed'),
('S12','빽다방','paik_price','언론(뉴스핌)','2025-05-15','2025-05-22부터 HOT 아메리카노 1,700원; 배달가격 제외','reported'),
('S13','텐퍼센트커피','ten_story','공식 홈페이지','게시일 미표기','상위 10% 스페셜티 주장; 다크 4개국·미디엄 3개국; 강·중배전 선택','claimed'),
('S14','텐퍼센트커피','ten_hot_store','매장정보 재게시(다이닝코드)','게시·적용일 미확인','울산비즈파크점 Regular/hot 아메리카노 2,500원; 전국 공통가격으로 일반화 안 함','reported'),
('S15','텐퍼센트커피','ten_price','매장 주문 플랫폼(패스오더)','게시일 미표기','은평구청점 아메리카노 2,500원; 온도 구분이 없어 HOT 분석에서는 제외','verified'),
('S16','텐퍼센트커피','ten_current_menu','매장 주문 플랫폼(패스오더)','게시일 미표기','정관제일점 아메리카노 2,000원; 온도 구분 미확인·100원 프로모션 제외','verified'),
('S17','컴포즈커피','compose_price','언론(한국경제)','2025-02-03','2025-02-13 ICE 1,800원; HOT 기존 1,500원 유지','reported'),
('S18','컴포즈커피','compose_exhibition','공식 전시회 참가기업 소개','2023년 전시회','계열사 로스팅 공장·비터홀릭; 브라질·콜롬비아·에티오피아, 세부 비율은 사용하지 않음','reported'),
('S19','컴포즈커피','compose_external','전문 매체(더피알)','게시일 확인 불가','비터홀릭 스페셜티 블렌딩·3개국·본사 로스팅 설명','reported'),
('S20','컴포즈커피','compose_bsca_news','언론(세계일보/다음)','2025-01-23','브라질 생두 BSCA 인증 사용 보도; 현재 로트 인증서·전체 블렌드 점수로 확대하지 않음','reported'),
('S21','투썸플레이스','twosome_home','공식 홈페이지','게시일 미표기','디저트 카페·매장 경험·전문가 교육 센터 안내','verified'),
('S22','투썸플레이스','twosome_hot_price_check','교환권 유통(SK플래닛/11번가)','게시일 미표기','HOT 아메리카노 R 4,700원 일반 표시가; 할인·포인트 혜택은 제외. HOT 메뉴 연결 보조 확인에만 사용','reported'),
('S23','파스쿠찌','pascucci_hot_tabling','매장 정보 플랫폼(테이블링)','게시일 미표기','세종라온점 아메리카노 HOT 4,700원; 보도 가격의 HOT 연결 보완, 실결제 아님','reported'),
]
SPECS += [
('S24','빽다방','paik_official_20_reaudit','공식 창업 안내','게시일 미표기','브라질 파젠다 엄 스페셜티 20% 배합 및 로스팅 후 5–15일 사용 안내','claimed'),
('S25','빽다방','paik_farm_2026_reaudit','현장 취재(데일리안)','2026-06-01','현재 시그니처: 브라질 벨로소 DOT·파젠다 엄 내추럴·파젠다 엄 펄프드 내추럴 3종','reported'),
('S26','빽다방·컴포즈커피','specialty_ratios_2026_reaudit','취재 기사(아이뉴스24)','2026-03-15','빽다방 스페셜티 20%; 컴포즈 미나스제라이스 스페셜티 5%, 해당 구성 원두 82점 보도','reported'),
('S27','컴포즈커피','compose_2026_reaudit','기업 홍보 인터뷰(NYF K-NBA)','2026-04-09','비터홀릭 브라질·콜롬비아·에티오피아; 브라질 BSCA 원두 및 자체 로스팅 안내','claimed'),
('S28','폴 바셋','paul_signature_reaudit','공식 원두 납품 안내','게시일 미표기','시그니처 블렌드: 브라질·에티오피아, 국내 전용 로스팅 공장','verified'),
('S29','폴 바셋','paul_principles_reaudit','공식 브랜드 원칙','게시일 미표기','브라질·에티오피아 생두 선별, 국내 로스팅 후 3–14일 사용, 항온·항습 관리','claimed'),
('S30','폴 바셋','paul_hot_reaudit','공식 HOT 메뉴','게시일 미표기','HOT 아메리카노 Standard 360mL, 시그니처 블렌드 사용을 명시','verified'),
('S31','폴 바셋','paul_price_reaudit','교환권 유통(11번가)','게시일 미표기','아메리카노 Standard 4,700원 표시가; 공식 HOT Standard 메뉴와 연결, 실결제 아님','reported'),
('S32','폴 바셋','paul_hold_price_reaudit','언론(뉴스핌)','2025-01-16','2025-01-23 가격 조정에서 아메리카노 가격 동결 보도','reported'),
]

def main():
    for p in ['data','analysis','research','presentation/assets']: (R/p).mkdir(parents=True,exist_ok=True)
    sources=[];registry={}
    for sid,brand,slug,typ,pub,claim,status in SPECS:
        f=R/f'data/firecrawl/{slug}.json'
        if not f.exists():print('PENDING',slug);continue
        j=json.loads(f.read_text(encoding='utf-8'));md=j['data'].get('markdown','')
        assert j['success'] and '요청한 웹페이지의 이름이 바뀌었거나' not in md,slug
        row=dict(출처ID=sid,브랜드명=brand,조사항목=claim.split(';')[0],확인된내용=claim,출처URL=j['url'],출처종류=typ,게시일=pub,수집일=DATE,실제수집시각=j['collected_at'],신뢰등급=status,원문파일=f'data/firecrawl/{slug}.md')
        sources.append(row);registry[sid]=row
    pd.DataFrame(sources).to_csv(R/'data/sources.csv',index=False,encoding='utf-8-sig')
    facts=[]
    def fact(b,field,value,sids,status='verified',scope='일반 비디카페인 매장용 원두',note=''):
        for sid in sids.split('|'):
            assert sid in registry,sid
        facts.append(dict(브랜드명=b,조사항목=field,값=value,검증상태=status,출처ID=sids,출처URL=' | '.join(registry[s]['출처URL'] for s in sids.split('|')),적용범위=scope,비고=note,수집일=DATE))
    brands=['스타벅스','투썸플레이스','폴 바셋','빽다방','텐퍼센트커피','컴포즈커피']
    bean_rows=[
      ['에스프레소 로스트',100,0,'라틴 아메리카·아시아/태평양(본문); 하단 아프리카/아라비아 표기 충돌','다크','스페셜티 사용 여부 미확인','C.A.F.E. Practices 윤리 구매 안내; 독립 관능점수 미확인','캐러멜·강한 바디','S01|S02|S03','verified'],
      ['블랙그라운드 / 아로마노트',None,None,'블랙: 콜롬비아·브라질·파푸아뉴기니 / 아로마: 에티오피아·과테말라','다크 / 미디엄','현재 블렌드의 스페셜티 주장 미확인','HACCP 공정관리 안내·내부 Q-Grader; 독립 관능점수 미확인','블랙: 초콜릿·견과·스모키 / 아로마: 과일·꽃','S06|S07','verified'],
      ['골든색(Golden Sack)',None,None,U,'한국 골든색 정확한 배전 단계 미확인; 전통 설명: 미디엄 슬로우 로스팅','프리미엄이라는 브랜드 표현','내부 연구원·소비자 테스트 설명; 외부 점수 미확인','말린 과일·밀크초콜릿·브라운슈가·아몬드','S09','verified'],
      ['시그니처 블렌딩',None,None,'브라질·파젠다 엄 농장 원두 활용(상세 구성·비율 미공개)','단계 미확인(공식 그래픽 별도)','스페셜티 원두 활용 블렌딩 주장','SCA 80점 이상은 일반 정의; 실제 블렌드·로트 점수 미공개','시나몬·브라운슈가·다크초콜릿·견과','S11','claimed'],
      ['다크 / 미디엄',None,None,'다크: 브라질·콜롬비아·과테말라·에티오피아 / 미디엄: 과테말라·콜롬비아·에티오피아','다크: 딥 로스팅(강배전) / 미디엄: 라이트 로스팅(중배전), 공식 용어 병기','상위 10% 스페셜티 블렌딩 주장','개별 로트 평가표·독립 SCA 점수 미확인','다크: 초콜릿·쌉싸름 / 미디엄: 과일·산미(매장 설명)','S13|S15','claimed'],
      ['비터홀릭',None,None,'브라질·콜롬비아·에티오피아(외부 기업 소개)','정확한 단계 미확인; 계열사 로스팅 공장 소개','스페셜티 블렌딩 보도','브라질 생두 BSCA 인증 사용 보도; 현재 로트 인증서 미확인','고소함·토스티·초콜릿 계열','S18|S19|S20','reported'],
    ]
    bean_rows[2]=['시그니처 블렌드',None,None,'브라질·에티오피아','공식 비교 자료에서 단계 미확보; 국내 전용 공장 로스팅','스페셜티 생두 직접 선별 주장','매장 전체 블렌드의 독립 평가표 미확보','초콜릿의 단맛·산미·풍부한 바디','S28|S29|S30','verified']
    bean_rows[3]=['시그니처 블렌드',None,None,'브라질: 벨로소 DOT·파젠다 엄 내추럴·파젠다 엄 펄프드 내추럴(2026 현장 보도)','단계 미확보; 로스팅 후 5–15일 사용 안내','파젠다 엄 스페셜티 원두 20% 배합(공식 안내)','구성 원두의 개별 평가표 및 완성 블렌드 점수 미확보','시나몬·브라운슈가·다크초콜릿·견과','S11|S24|S25|S26','reported']
    bean_rows[5]=['비터홀릭',None,None,'브라질·콜롬비아·에티오피아(2026 기업 인터뷰); 스페셜티 구성분 브라질 미나스제라이스(취재)','정확한 단계 미확보; 자체 로스팅 안내','스페셜티 구성 원두 5% 배합 보도','해당 구성 원두 SCA 82점 보도; 전체 블렌드 점수 아님·평가표 미확보','고소함·토스티·초콜릿 계열','S26|S27|S20','reported']
    rows=[]
    for i,(b,v) in enumerate(zip(brands,bean_rows)):
        blend,ara,rob,orig,roast,spec,cert,taste,sids,status=v
        rows.append(dict(브랜드명=b,그룹='A 일반 프랜차이즈' if i<3 else 'B 가성비 포지셔닝',블렌드명=blend,아라비카비율=ara,로부스타비율=rob,원산지=orig,원산지별비율=U,로스팅=roast,스페셜티주장=spec,인증_평가점수=cert,향미=taste,공개여부='비율 확인' if ara is not None else '비율 근거 미확보(기업의 비공개 선언 아님)',검증상태=status,출처ID=sids,출처URL=' | '.join(registry[s]['출처URL'] for s in sids.split('|')),기준일='자료별 상이; 게시일 미표기 자료 포함',수집일=DATE))
        for field,val in [('블렌드명',blend),('원산지',orig),('로스팅',roast)]:fact(b,field,val,sids,'reported' if b in ['컴포즈커피','빽다방'] else 'verified',note='verified는 공식 문구 확인이며 독립 품질 검증이 아님')
        fact(b,'아라비카비율',str(ara) if ara is not None else U,sids,'verified' if ara is not None else 'unknown',note='100% 아라비카의 로부스타 0%는 그 문구의 논리적 보완; 다른 결측치는 0으로 대체하지 않음')
        fact(b,'스페셜티',spec,sids,'claimed' if b in ['빽다방','텐퍼센트커피'] else 'reported' if b=='컴포즈커피' else 'unknown')
        fact(b,'독립관능점수','확인 불가',sids,'unknown',note='점수가 없다는 단정이 아니라 이번 조사 자료에서 확보하지 못함')
    beans=pd.DataFrame(rows);beans.to_csv(R/'data/brand_beans.csv',index=False,encoding='utf-8-sig')
    prices=[]
    specs=[(4700,'Tall',355,'S04|S05','2025-01-24','일반 매장 가격 보도(특수매장 제외)','reported'),(4700,'Regular',None,'S08|S22','2025-03-26','일반 매장 가격 보도; HOT 교환권 표시가 보조 확인','reported'),(4700,'Standard',360,'S28|S30|S31|S32','적용일 미표기; 2025-01 동결 보도','일반 Standard 교환권 표시가와 공식 HOT 메뉴 연결; 실결제 아님','reported'),(1700,'기본',None,'S12','2025-05-22','일반 매장 가격 보도(배달 제외)','reported'),(2500,'Regular',None,'S14','적용일 미확인','울산 중구 종가로 406-21, 울산비즈파크점 메뉴 재게시','reported'),(1500,'기본',None,'S17','2025-02-13','일반 매장 HOT 동결 보도','reported')]
    for i,(b,v) in enumerate(zip(brands,specs)):
        price,size,ml,sids,effective,store,status=v
        prices.append(dict(관측ID=f'P{i+1:02}',브랜드명=b,메뉴='아메리카노',HOT_ICE='HOT',기본가격=price,사이즈=size,용량_mL=ml,샷수=None,원두투입량_g=None,매장위치=store,확인일=DATE,적용기준일=effective,출처ID=sids,출처URL=' | '.join(registry[s]['출처URL'] for s in sids.split('|')),검증상태=status,분석포함=True,비고='동일시점 영수증 조사 아님; 스타벅스 Tall은 최소 판매 Short와 다름' if i==0 else '자료 시점·매장 범위가 달라 최신 전국 동일가 보장 안 됨'))
        fact(b,'HOT가격',price,sids,status,store,'적용일 '+effective)
    for sid,price,store in [('S15',2500,'은평구청점'),('S16',2000,'정관제일점')]:
        prices.append(dict(관측ID='P07' if sid=='S15' else 'P08',브랜드명='텐퍼센트커피',메뉴='아메리카노',HOT_ICE='온도 미확인',기본가격=price,사이즈='기본',용량_mL=None,샷수=None,원두투입량_g=None,매장위치=store,확인일=DATE,적용기준일='미확인',출처ID=sid,출처URL=registry[sid]['출처URL'],검증상태='verified',분석포함=False,비고='온도 미확인으로 HOT 비교 제외; 100원 이벤트가 아닌 일반 메뉴값'))
    pdf=pd.DataFrame(prices);pdf.to_csv(R/'data/price_observations.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(facts).to_csv(R/'data/facts.csv',index=False,encoding='utf-8-sig')
    comp=beans.merge(pdf[pdf['분석포함']][['브랜드명','기본가격','용량_mL','적용기준일','매장위치','관측ID']],on='브랜드명',validate='one_to_one')
    comp['100mL당가격']=comp['기본가격']/comp['용량_mL']*100
    comp.to_csv(R/'data/comparison.csv',index=False,encoding='utf-8-sig')
    metrics=dict(collected=DATE,brands=6,source_count=len(sources),price_observations=len(prices),hot_observations=6,maximum=int(comp['기본가격'].max()),minimum=int(comp['기본가격'].min()),gap=int(comp['기본가격'].max()-comp['기본가격'].min()),max_min_ratio=float(comp['기본가격'].max()/comp['기본가격'].min()),group_a_mean=float(comp.iloc[:3]['기본가격'].mean()),group_b_mean=float(comp.iloc[3:]['기본가격'].mean()),breed_ratio_confirmed=int(comp['아라비카비율'].notna().sum()),origin_ratio_confirmed=0,independent_sensory_scores_obtained=0,volume_confirmed=int(comp['용량_mL'].notna().sum()),price_basis='서로 다른 적용일의 공개 HOT 가격 관측치. 텐퍼센트는 특정 매장 재게시값. 전국 동시점 시장 평균 아님.')
    (R/'analysis/metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    (R/'research/reviewed_evidence.json').write_text(json.dumps(dict(sources=sources,facts=facts,beans=beans.where(pd.notna(beans),None).to_dict('records'),prices=prices,metrics=metrics),ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    audit=[]
    for f in (R/'data/firecrawl').glob('*.json'):
        j=json.loads(f.read_text(encoding='utf-8'));md=j.get('data',{}).get('markdown','');soft=any(t in md for t in ['요청한 웹페이지의 이름이 바뀌었거나','등록된 영양정보가 없습니다'])
        audit.append(dict(file=f.name,url=j['url'],http=j['page_status'],content_valid=bool(j['success']) and not soft,reason='soft 404' if soft else 'HTTP error' if not j['success'] else '본문 별도 검토',collected_at=j['collected_at']))
    pd.DataFrame(audit).to_csv(R/'data/collection_log.csv',index=False,encoding='utf-8-sig')
    from origin_audit import main as audit_origins
    audit_origins()
    evidence_path=R/'research/reviewed_evidence.json'
    evidence=json.loads(evidence_path.read_text(encoding='utf-8'))
    evidence['facts']=pd.read_csv(R/'data/facts.csv').astype(object).where(lambda x:pd.notna(x),None).to_dict('records')
    evidence['origin_audit']=pd.read_csv(R/'data/origin_audit.csv').fillna('이번 조사에서 미확보').to_dict('records')
    evidence['specialty_components']=pd.read_csv(R/'data/specialty_components.csv').astype(object).where(lambda x:pd.notna(x),None).to_dict('records')
    evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
