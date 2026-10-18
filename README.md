# 비싼 커피는 정말 더 좋은 원두를 사용할까?

2026-10-18 실제 웹 원문을 재검토한 6개 브랜드 비교. **파스쿠찌를 유사 가격대의 폴 바셋으로 교체한 수정본**이다. 원두 생산국과 매장 메뉴를 연결하고, 배합 함량과 품질 점수를 구분했다. 공개 정보만으로 절대적 품질 순위·공급 원가·인과관계를 산출하지 않는다.

대상: 스타벅스·투썸플레이스·폴 바셋 / 빽다방·텐퍼센트커피·컴포즈커피. 공식 원두 설명, 공식 HOT 메뉴, 2026 현장 취재와 기업 인터뷰를 Firecrawl로 수집했다. 파스쿠찌 미확보와 표본 교체 편향, 스타벅스 국가 구성 미완료를 숨기지 않았다.

## 핵심 결과

|브랜드·블렌드|생두 생산국·지역|근거 상태|출처|
|---|---|---|---|
|스타벅스 / 에스프레소 로스트|라틴 아메리카·아시아/태평양(본문)|verified|S01|S02|
|투썸플레이스 / 블랙그라운드|콜롬비아·브라질·파푸아뉴기니|verified|S06|S07|
|투썸플레이스 / 아로마노트|에티오피아·과테말라|verified|S06|S07|
|폴 바셋 / 시그니처 블렌드|브라질·에티오피아|verified|S28|S29|S30|
|빽다방 / 시그니처 블렌드|브라질|reported|S24|S25|S26|
|텐퍼센트커피 / 다크|브라질·콜롬비아·과테말라·에티오피아|verified|S13|
|텐퍼센트커피 / 미디엄|과테말라·콜롬비아·에티오피아|verified|S13|
|컴포즈커피 / 비터홀릭|브라질·콜롬비아·에티오피아|reported|S26|S27|

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

전체 출처 32개에는 제외한 파스쿠찌의 조사 이력도 있다. S번호→원문 Markdown·URL·수집일, facts.csv→필드별 상태를 확인한다. verified=공식/원문 문구 확인, reported=외부 취재·보도, claimed=자체 품질·관리 주장, unknown=미확보. 원문 확인이 독립 시험을 의미하지 않는다.

발표 슬라이드: https://ancoded1234.github.io/coffee-brand-analysis/

GitHub 저장소: https://github.com/ancoded1234/coffee-brand-analysis

사용자의 공개 배포 요청에 따라 GitHub CLI와 Pages REST API로 main 브랜치의 /docs를 배포한다. `scripts/prepare_pages.py`로 HTML·로컬 에셋을 복사한다. 원문 크롤링 전문·기존 .env·인증 파일·가상환경은 공개 저장소에서 제외한다. 로컬 확인: `python -m http.server 8000 --directory docs`.
