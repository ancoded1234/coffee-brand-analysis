from pathlib import Path
import json,hashlib,zipfile
import pandas as pd
from PIL import Image
import av
R=Path(__file__).resolve().parents[1];P=R/'presentation';M=json.loads((R/'analysis/metrics.json').read_text(encoding='utf-8'));C=pd.read_csv(R/'data/comparison.csv');S=pd.read_csv(R/'data/sources.csv')
prompt='Create a 16:9 landscape editorial photograph for a university coffee data journalism presentation. A single unbranded ivory ceramic espresso cup with rich dark coffee and delicate crema, a few roasted coffee beans on textured warm beige paper, sculptural morning side light, espresso brown and cream palette, premium minimalist coffee magazine aesthetic, realistic photographic texture. Place cup on the right half, generous clean negative space on left for a headline. No text, no letters, no logos, no people. Still image.'
(R/'research/asset_provenance.md').write_text(f'''# 비주얼·라이브러리 출처

- 표지: Google Flow 웹 UI에서 사용자가 로그인한 계정으로 새 프로젝트 생성 후 직접 생성·다운로드.
- 프로젝트: https://flow.google.com/project/12b5d2ce-80a1-48b8-bc60-030387dc0204 (계정 소유자용 작업 링크, 공개 제출 URL 아님)
- 모델 UI 표기: Nano Banana 2.1. 생성일 2026-10-18. 비율 16:9. 1개 출력. 생성 UI 0크레딧 표시.
- 파일: `presentation/assets/coffee-editorial-flow.jpg`. 사진은 실제 브랜드 제품·원두를 촬영한 것이 아닌 AI 생성 이미지이며 모든 사용 위치에 표기.
- 사용 권한: 사용자 요청에 따라 본인 로그인 환경에서 생성한 학습 발표용 에셋. 타 브랜드 로고·제품 사진은 사용하지 않음. Google 서비스 약관상의 권리는 별도 적용됨.
- 프롬프트: {prompt}
- 모션: Manim Community 0.22.0, 직접 작성한 코드와 CSV로 4개 영상 렌더링. 가상의 품질 점수는 사용하지 않음.
- 정적 차트: Seaborn 0.13.2, Matplotlib. 원본 PNG·SVG 모두 `analysis/figures/`.
- HTML 모션: Anime.js, npm CDN 배포 번들 로컬 저장. 라이선스 `presentation/assets/anime-LICENSE.txt`. 인터넷 없이 발표 가능.
- UI 참고: 사용자가 설치한 부모 경로 `DESIGN.md`의 여백·정보 위계·부드러운 카드·컨트롤을 참고. 커피 브라운/크림이라는 사용자 색상 지침을 우선.
- PowerPoint: 맑은 고딕·Arial·Georgia. 폰트 파일은 재배포하지 않음. 표지 외 텍스트·표·다이어그램은 수정 가능. 가격·그룹 평균 차트는 네이티브 Office 차트. 9번 그래프는 Seaborn 이미지이므로 데이터 수정은 Python 원본으로 재생성.
''',encoding='utf-8')
video_report=[]
for f in (P/'assets').glob('*.mp4'):
    con=av.open(str(f));stream=con.streams.video[0];frames=list(con.decode(video=0));assert frames
    frames[-1].to_image().save(P/'assets'/f'{f.stem}-poster.jpg')
    video_report.append(dict(file=f.name,width=stream.width,height=stream.height,frames=len(frames),duration_seconds=round(len(frames)/float(stream.average_rate),2)))
    con.close()
(R/'analysis/qa/video_validation.json').write_text(json.dumps(video_report,indent=2),encoding='utf-8')
O=pd.read_csv(R/'data/origin_audit.csv');D=pd.read_csv(R/'data/specialty_components.csv')
origin_table='|브랜드·블렌드|생두 생산국·지역|근거 상태|출처|\n|---|---|---|---|\n'+'\n'.join(f"|{r.브랜드명} / {r.블렌드명}|{r.생두생산국_지역}|{r.검증상태}|{r.출처ID}|" for r in O.itertuples())
price_table='|브랜드|HOT 관측값|용량 mL|기준|\n|---|---:|---:|---|\n'+'\n'.join(f"|{r.브랜드명}|{r.기본가격:,}원|{int(r.용량_mL) if pd.notna(r.용량_mL) else '미확보'}|{r.적용기준일}|" for r in C.itertuples())
insights=f'''# 수정 분석 — 비싼 커피는 정말 더 좋은 원두를 사용할까?

수집·재조사: 2026-10-18. 최초 조사는 원두 생산국·농장과 매장 제품의 연결이 부족했고, 빽다방·컴포즈의 2026년 구성 정보를 누락했다. 출처 개수만으로 조사가 완료됐다고 판단할 수 없다. 아래는 근거를 다시 검토한 수정본이다.

## 대상 교체와 선정 한계

파스쿠찌 → **폴 바셋**. 사용자의 대체 지시에 따라 유사한 4,700원대 공개 관측 가격 중 공식 생산국과 HOT 메뉴 사용 블렌드가 연결되는 브랜드를 선정했다(S28·S30·S31). 파스쿠찌의 현재 한국 매장 골든삭 생산국은 미확보다. 전통 80:20, 이탈리아 제조, RTD 캔의 원재료 비율은 한국 매장 골든삭의 생산국·배합비 근거로 사용할 수 없다. 제외 자료도 sources.csv에 보존했다.

공개 정보 접근성을 기준으로 표본을 바꿨으므로 정보 공개가 많은 브랜드가 선택되는 편향이 있다. 6개를 시장 대표 표본으로 일반화하지 않는다. 스타벅스는 공식 지역 설명은 확보했으나 국가 단위 추적을 완료하지 못해 그 한계를 명시하고 유지했다.

## 1. 원두가 어디서 오는가

{origin_table}

빽다방은 2026-06-01 현장 취재에서 **브라질 벨로소 DOT·파젠다 엄 내추럴·파젠다 엄 펄프드 내추럴** 3종을 확인했다(S25). 공식 창업 자료도 브라질 파젠다 엄과 스페셜티 20% 배합을 명시한다(S24). 3종의 개별 배합표는 확보하지 못했다.

컴포즈 비터홀릭은 2026 기업 인터뷰의 브라질·콜롬비아·에티오피아 구성(S27)과 2026-03-15 취재의 브라질 미나스제라이스 스페셜티 구성분(S26)을 구분했다. 공식 사이트의 접근 제한 때문에 이것을 공식 원문 직접 확인이라고 표시하지 않았다.

투썸·텐퍼센트는 옵션별로 국가가 달라 별도 행으로 보존했다. 폴 바셋의 국내 로스팅과 브라질·에티오피아 생산국도 별도 필드다. 스타벅스는 제품 본문 지역과 하단 Origin이 충돌해 국가 구성을 확정하지 않았다(S02). 상세 농장·제품 적용·누락 사유·URL·기준일은 `data/origin_audit.csv`에 있다.

## 2. 비율과 점수의 적용 범위

- 빽다방 **20%**: 공식 페이지의 파젠다 엄 스페셜티 배합 안내. 문구는 확인했지만 평가표를 독립 검증한 것은 아니므로 품질 주장은 claimed. 2026 취재와 교차 확인.
- 컴포즈 **5%**: 2026 취재 보도 reported. **82점**도 해당 스페셜티 구성 원두의 보도값이며, 전체 비터홀릭·완성 음료의 점수가 아니다. 평가 원본·현재 로트 인증서는 미확보.
- 텐퍼센트 ‘상위 10%’는 품종 함량이나 스페셜티 배합률 10%가 아니다. 함량 차트에 사용하지 않았다.
- 스타벅스 아라비카 전용 정책 외 현재 분석 블렌드의 품종 비율은 근거 미확보. 국가별 전체 배합 비율도 미확보. 숫자 결측은 NaN, 표시명은 ‘미확보’다. 기업이 비공개를 선언했다고 단정하지 않는다.

## 3. 가격 비교

{price_table}

선정 자료의 최고 4,700원·최저 1,500원, 차이 3,200원, **3.13배**. A그룹 단순 평균 4,700원, B 1,900원. 서로 다른 적용일·매장·사이즈 자료의 기술통계이며 최신 전국 실결제 가격·판매량 가중 시장 평균이 아니다. 폴 바셋은 Standard 교환권 표시가를 공식 HOT Standard와 연결한 보조 관측이며 영수증이 아니다. 텐퍼센트는 울산비즈파크점 재게시 값이다.

공식 HOT 용량은 스타벅스 Tall 355mL와 폴 바셋 Standard 360mL 확인. 각각 100mL당 약 1,323.94원·1,305.56원이지만 나머지 용량이 없어 6개 순위는 만들지 않는다. Tall은 최소 판매 Short가 아니다. 샷수·메뉴별 실제 투입량은 비교 가능한 확정값을 확보하지 못했다. 폴 바셋 공통 5S의 26g 안내를 개별 HOT 메뉴 투입량으로 전용하지 않았다.

## 4. 질문에 답할 수 있는 범위

높은 가격대의 폴 바셋에도 스페셜티 선별 주장이 있고, 가성비 빽다방·컴포즈에도 구체적 스페셜티 구성 함량이 공개·보도됐다. **스페셜티 원두 사용이 높은 판매가격의 브랜드에만 있는 특징은 아니다.** 다만 함량의 차이를 독립 품질 순위로 바꿀 수 없다.

산지·농장·로스팅은 추적 가능한 특성이지만 그 자체로 맛의 우열을 정하지 못한다. C.A.F.E. Practices 윤리 구매, HACCP 공정 안전, 내부 Q-Grader, BSCA 생두 보도도 서로 다른 지표다. 독립적인 동일 조건의 완성 블렌드 평가표와 공급가가 없어 ‘비싸면 더 좋은 원두’라는 가설은 핵심 품질 측정에서 미검증이다. 싸면 더 좋다거나 차이가 없다는 반대 결론도 내리지 않는다.

매장 공간·서비스·제조 관리가 가격에 반영될 수 있다는 개념은 분리해 보여주되 기여율·임대료·마진은 계산하지 않았다. 후속 과제는 같은 날 같은 지역의 HOT 영수증·실제 부피·옵션을 기록하고 익명 코드·무작위 순서·동일 온도 반복 시음과 독립 커핑을 실시하는 것이다.
'''
(R/'analysis/insights.md').write_text(insights,encoding='utf-8')
log=pd.read_csv(R/'data/collection_log.csv')
quality=f'''# 데이터 품질 검수 — 수정본

- 조사일 2026-10-18. 근거 등록 {len(S)}개(제외 브랜드의 조사 근거 포함), 분석 브랜드 6개, 옵션별 원두 추적 {len(O)}행, 가격 8건 중 HOT 비교 6건.
- 최초 조사 누락: 빽다방 2026 농장·가공방식 3종 및 공식 스페셜티 20%, 컴포즈 2026 스페셜티 구성분 5%·해당 원두 82점 보도. 이번 수정에 반영.
- 파스쿠찌 현재 한국 매장 생산국 미확보 → 유사 가격대 폴 바셋으로 교체. 선정 사유와 정보 접근성에 따른 표본 편향을 기록. 제외 브랜드 자료를 성공한 매장 원두 근거로 사용하지 않음.
- ‘미공개’와 ‘이번 조사 미확보’를 구분. 기업의 비공개 선언을 확인하지 못한 필드는 미확보라고 표현. 값 누락을 0으로 대체하지 않음.
- 국가·지역·농장·가공방식·로스팅 장소·품종 비율·스페셜티 함량을 분리. 공식 소개 확인은 independently measured 품질 검증이 아님.
- 컴포즈 원산지 3개국은 기업 홍보 인터뷰, 5%·82점은 외부 취재. 82점을 전체 블렌드나 매장 한 잔 점수로 확대하지 않음. 독립 평가표 미확보.
- 스타벅스 공식 제품 본문과 Origin 충돌을 남김. 국가별 구성과 농장 추적은 미완료. 텐퍼센트 상위 10%를 함량으로 사용하지 않음.
- 최신 수집일과 가격 적용일은 다름. 2025년 보도와 날짜 미표기 교환권·매장 재게시 자료를 2026 전국 최신 실결제 가격으로 표시하지 않음.
- 폴 바셋 HOT Standard 360mL와 시그니처 사용을 공식 메뉴로 확인. 26g 공통 설명은 이 메뉴의 투입량 확정값으로 사용하지 않음. 용량 확정 2/6, 샷수·메뉴별 투입량 미확보.
- Firecrawl 로그 {len(log)}건. HTTP 200만으로 본문 성공으로 판단하지 않고 소프트404·‘등록된 영양정보가 없습니다’ 등 빈 내용은 탈락시킴. `collection_log.csv`에 기록.
- 공식 접근 제한·403은 대체 언론·기업 소개로 보완하고 reported/claimed 표시. 로그인·CAPTCHA·국가 제한을 우회하지 않음. 공개 자료만 소량 직렬 요청하고 API 429는 제한 재시도·대기.
- 기존 부모 `.env`는 python-dotenv로 읽기만 하며 새로 만들거나 변경하지 않음. 키는 출력하지 않고 최종 파일의 비밀정보 포함 여부도 검사.
- 실제 PowerPoint 열기·재열기·PDF 및 13장 PNG 내보내기, 네이티브 차트 데이터 확인은 qa/powerpoint_validation.json. HTML 데스크톱·모바일 13장·키보드·노트·출처·모션 검수는 qa/browser_validation.json.
- source_count나 파일 완성은 연구 완성도·원두 품질의 대리 지표가 아님. 독립 품질 비교·공급가·농장별 전체 배합표가 남은 한계다.
'''
(R/'analysis/data_quality_report.md').write_text(quality,encoding='utf-8')
readme=f'''# 비싼 커피는 정말 더 좋은 원두를 사용할까?

2026-10-18 실제 웹 원문을 재검토한 6개 브랜드 비교. **파스쿠찌를 유사 가격대의 폴 바셋으로 교체한 수정본**이다. 원두 생산국과 매장 메뉴를 연결하고, 배합 함량과 품질 점수를 구분했다. 공개 정보만으로 절대적 품질 순위·공급 원가·인과관계를 산출하지 않는다.

대상: 스타벅스·투썸플레이스·폴 바셋 / 빽다방·텐퍼센트커피·컴포즈커피. 공식 원두 설명, 공식 HOT 메뉴, 2026 현장 취재와 기업 인터뷰를 Firecrawl로 수집했다. 파스쿠찌 미확보와 표본 교체 편향, 스타벅스 국가 구성 미완료를 숨기지 않았다.

## 핵심 결과

{origin_table}

빽다방 스페셜티 구성분 20%(공식 자체 안내), 컴포즈 5%(2026 취재 보도). 컴포즈 82점은 해당 구성 원두의 보도값이며 전체 블렌드 점수가 아니다. 텐퍼센트 상위 10%는 배합률이 아니다.

선정 HOT 가격은 1,500–4,700원, 차이 3,200원·3.13배, 그룹 단순 평균 4,700원·1,900원. 서로 다른 적용일의 보도·특정 매장·교환권 관측으로 최신 전국 동시점 실결제나 동일 용량 비교가 아니다. 공식 HOT 용량 확인은 355mL·360mL의 2개 브랜드다.

스페셜티 사용은 비싼 브랜드만의 특징이 아니지만, 동일 조건의 독립 맛 평가와 공급가가 없어 가격-절대 품질 가설은 미검증이다.

## 결과물

- `presentation/coffee_brand_analysis.pptx`: 16:9, 13장, 수정 가능한 텍스트·표·가격 Office 차트 2개와 네이티브 모션.
- `presentation/coffee_brand_analysis.pdf`: 실제 PowerPoint가 내보낸 정적 제출본.
- `presentation/index.html`: 로컬 Anime.js 그래프, Manim 4개 영상, 방향키·버튼·전체화면·노트·출처. 더블클릭 또는 HTTP 서버로 실행.
- `presentation/speaker_notes.md`: 각 슬라이드 적용 범위와 출처 URL. PPT에도 내장.
- 요청 데이터 4종: `data/brand_beans.csv`, `price_observations.csv`, `sources.csv`, `comparison.csv`.
- 재조사 근거: `data/origin_audit.csv`(옵션별 생산국·농장·제조 장소·시점·URL), `specialty_components.csv`, `brand_selection.csv`, `facts.csv`.
- `data/firecrawl/`: 성공·실패 실제 원문과 수집시각. `analysis/insights.md`, `data_quality_report.md`: 수정 결과·한계.
- `analysis/figures/`: Seaborn PNG·SVG 6종. `analysis/qa/`: PowerPoint·브라우저·영상 검수.
- `research/asset_provenance.md`: 사용자 로그인 Google Flow에서 직접 생성·다운로드한 표지 이력. 실제 브랜드 제품 사진이 아닌 AI 이미지.

## 실행

Windows, Python 3.12. 기존 부모 `.env`의 키를 읽기만 한다. `.env`는 Git 제외. requirements.txt로 환경을 재현한다.

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
.venv/Scripts/python.exe scripts/build_data.py
.venv/Scripts/python.exe scripts/figures.py
.venv/Scripts/python.exe scripts/motion.py
.venv/Scripts/python.exe scripts/presentation.py
.venv/Scripts/python.exe scripts/html_deck.py
.venv/Scripts/python.exe scripts/office_qa.py
.venv/Scripts/python.exe scripts/browser_qa.py
.venv/Scripts/python.exe scripts/reports.py
.venv/Scripts/python.exe scripts/finalize.py
```

`collect.py URL CACHE_SLUG`는 캐시가 없을 때만 실제 Firecrawl을 호출한다. `build_data.py`는 검토된 근거를 CSV로 재현하고 `origin_audit.py`를 함께 실행한다. `revise_research.py`는 최초 초안에서 수정할 때 한 번 사용한 기록용 마이그레이션이며 다시 실행하지 않는다. Microsoft PowerPoint COM과 Playwright Chromium이 검수에 필요하다.

전체 출처 {len(S)}개에는 제외한 파스쿠찌의 조사 이력도 있다. S번호→원문 Markdown·URL·수집일, facts.csv→필드별 상태를 확인한다. verified=공식/원문 문구 확인, reported=외부 취재·보도, claimed=자체 품질·관리 주장, unknown=미확보. 원문 확인이 독립 시험을 의미하지 않는다.

공개 배포는 이번 커피 과제에서 요청되지 않아 GitHub 업로드·공개 URL을 만들지 않았다. 로컬 확인: `python -m http.server 8000 --directory presentation`. API 키·인증 파일·가상환경은 제출 ZIP에 포함하지 않는다.
'''
(R/'README.md').write_text(readme,encoding='utf-8')
if (R/'docs/index.html').exists():
    # Keep publication details when regenerating the research report after deployment.
    import runpy
    runpy.run_path(str(R/'scripts/prepare_pages.py'),run_name='__main__')
print('Corrected reports, notes provenance, README and video validation saved')
