"""Field-level origin evidence, with product scope kept separate from recipe ratios."""
from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]
def main():
    s=pd.read_csv(R/'data/sources.csv').set_index('출처ID'); out=[]
    def row(brand,blend,countries,farms,roast,ids,status,scope,limitation):
        out.append(dict(브랜드명=brand,블렌드명=blend,생두생산국_지역=countries,농장_가공방식=farms,로스팅장소=roast,국가별배합비='이번 조사에서 근거 미확보',검증상태=status,적용범위=scope,미확보_충돌사항=limitation,출처ID=ids,출처URL=' | '.join(s.loc[i,'출처URL'] for i in ids.split('|')),게시_기준일=' | '.join(s.loc[i,'게시일'] for i in ids.split('|')),수집일='2026-10-18'))
    row('스타벅스','에스프레소 로스트','라틴 아메리카·아시아/태평양(본문)','개별 농장 미확보','이번 근거에서 한국 공급 로스팅 공장 미확보','S01|S02','verified','한국 공식 에스프레소 로스트 제품 설명','동일 페이지 하단 Origin이 아프리카/아라비아로 달라 충돌. 국가 목록은 확정하지 않음')
    row('투썸플레이스','블랙그라운드','콜롬비아·브라질·파푸아뉴기니','개별 농장 미확보','자체 로스팅 플랜트(한국 공식 소개)','S06|S07','verified','매장 선택 블렌드; 아로마노트와 구분','공식 페이지 게시일 미표기. 국가별 비율·농장·로트 평가표 미확보')
    row('투썸플레이스','아로마노트','에티오피아·과테말라','에티오피아 내추럴 표기','자체 로스팅 플랜트(한국 공식 소개)','S06|S07','verified','매장 원두 옵션, 블랙그라운드와 혼합하지 않음','국가별 비율·농장·로트 평가표 미확보')
    row('폴 바셋','시그니처 블렌드','브라질·에티오피아','개별 농장 미확보','국내 전용 로스팅 팩토리','S28|S29|S30','verified','공식 HOT 아메리카노가 시그니처 사용을 명시','배합비·농장명·개별 로트 점수 미확보. 국내는 제조 장소이며 생두 산지가 아님')
    row('빽다방','시그니처 블렌드','브라질','벨로소 DOT / 파젠다 엄 내추럴 / 파젠다 엄 펄프드 내추럴','이번 근거에서 공장 소재지 미확보','S24|S25|S26','reported','2026-06-01 현장 취재의 현재 시그니처 3종; 공식 페이지가 파젠다 엄 산지·20%를 보완','농장별·가공방식별 전체 배합표 미확보. 20%는 스페셜티 구성분의 비율')
    row('텐퍼센트커피','다크','브라질·콜롬비아·과테말라·에티오피아','개별 농장 미확보','이번 근거에서 공장 소재지 미확보','S13','verified','공식 다크 블렌드; 미디엄 및 디카페인과 구분','상위 10%는 품종 함량·스페셜티 배합비가 아님. 국가별 비율 미확보')
    row('텐퍼센트커피','미디엄','과테말라·콜롬비아·에티오피아','개별 농장 미확보','이번 근거에서 공장 소재지 미확보','S13','verified','공식 미디엄 블렌드','국가별 비율·농장·개별 로트 평가표 미확보')
    row('컴포즈커피','비터홀릭','브라질·콜롬비아·에티오피아','스페셜티 구성분: 브라질 미나스제라이스 지역','자체 로스팅(2026 기업 인터뷰)','S26|S27','reported','2026 기업 인터뷰와 취재 기사. 공식 사이트 본문은 접근 제한으로 직접 확보 못함','5%·82점은 스페셜티 구성 원두 보도값. 전체 블렌드·음료 점수로 사용 불가; 평가표 미확보')
    pd.DataFrame(out).to_csv(R/'data/origin_audit.csv',index=False,encoding='utf-8-sig')
    specialty=pd.DataFrame([
        dict(브랜드명='빽다방',블렌드명='시그니처 블렌드',스페셜티구성분_pct=20,구성원두점수=None,검증상태='claimed',근거형태='공식 배합 안내 + 2026 취재 교차 확인',출처ID='S24|S25|S26',적용범위='브라질 파젠다 엄 스페셜티 구성분; 전체 품질 점수 아님'),
        dict(브랜드명='컴포즈커피',블렌드명='비터홀릭',스페셜티구성분_pct=5,구성원두점수=82,검증상태='reported',근거형태='2026-03-15 취재 보도',출처ID='S26',적용범위='브라질 미나스제라이스 스페셜티 구성 원두; 평가표 미확보·완성 블렌드 점수 아님'),
    ])
    specialty.to_csv(R/'data/specialty_components.csv',index=False,encoding='utf-8-sig')
    # Append precise component facts without promoting reported scores to independently measured quality.
    facts=pd.read_csv(R/'data/facts.csv')
    extra=[]
    for _,r in specialty.iterrows():
        for field,val in [('스페셜티구성분_pct',r['스페셜티구성분_pct']),('구성원두점수',r['구성원두점수'])]:
            if pd.isna(val):continue
            extra.append(dict(브랜드명=r['브랜드명'],조사항목=field,값=val,검증상태=r['검증상태'],출처ID=r['출처ID'],출처URL=' | '.join(s.loc[i,'출처URL'] for i in r['출처ID'].split('|')),적용범위=r['적용범위'],비고=r['근거형태'],수집일='2026-10-18'))
    facts=pd.concat([facts[~facts['조사항목'].isin(['스페셜티구성분_pct','구성원두점수'])],pd.DataFrame(extra)],ignore_index=True)
    facts.to_csv(R/'data/facts.csv',index=False,encoding='utf-8-sig')
    selected=pd.DataFrame([
      ['파스쿠찌','제외','현재 한국 골든삭의 생산국과 적용 범위를 확보하지 못함; 전통 80:20은 대체 근거가 아님','S09'],
      ['폴 바셋','대체 편입','유사한 4,700원대 관측 가격. 공식 생산국·시그니처와 HOT 메뉴 연결·360mL 확인','S28|S30|S31'],
      ['스타벅스','유지·지역 단위 제한','공식 지역 설명은 확보했으나 국가 단위 추적은 미완료. 그 한계를 명시','S01|S02'],
    ],columns=['브랜드명','선정결정','사유','출처ID'])
    selected.to_csv(R/'data/brand_selection.csv',index=False,encoding='utf-8-sig')
    print('Origin audit: 8 blend-specific rows, specialty components and selection rationale saved')
if __name__=='__main__':main()
