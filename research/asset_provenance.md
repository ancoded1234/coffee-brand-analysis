# 비주얼·라이브러리 출처

- 표지: Google Flow 웹 UI에서 사용자가 로그인한 계정으로 새 프로젝트 생성 후 직접 생성·다운로드.
- 프로젝트: https://flow.google.com/project/12b5d2ce-80a1-48b8-bc60-030387dc0204 (계정 소유자용 작업 링크, 공개 제출 URL 아님)
- 모델 UI 표기: Nano Banana 2.1. 생성일 2026-10-18. 비율 16:9. 1개 출력. 생성 UI 0크레딧 표시.
- 파일: `presentation/assets/coffee-editorial-flow.jpg`. 사진은 실제 브랜드 제품·원두를 촬영한 것이 아닌 AI 생성 이미지이며 모든 사용 위치에 표기.
- 사용 권한: 사용자 요청에 따라 본인 로그인 환경에서 생성한 학습 발표용 에셋. 타 브랜드 로고·제품 사진은 사용하지 않음. Google 서비스 약관상의 권리는 별도 적용됨.
- 프롬프트: Create a 16:9 landscape editorial photograph for a university coffee data journalism presentation. A single unbranded ivory ceramic espresso cup with rich dark coffee and delicate crema, a few roasted coffee beans on textured warm beige paper, sculptural morning side light, espresso brown and cream palette, premium minimalist coffee magazine aesthetic, realistic photographic texture. Place cup on the right half, generous clean negative space on left for a headline. No text, no letters, no logos, no people. Still image.
- 모션: Manim Community 0.22.0, 직접 작성한 코드와 CSV로 4개 영상 렌더링. 가상의 품질 점수는 사용하지 않음.
- 정적 차트: Seaborn 0.13.2, Matplotlib. 원본 PNG·SVG 모두 `analysis/figures/`.
- HTML 모션: Anime.js, npm CDN 배포 번들 로컬 저장. 라이선스 `presentation/assets/anime-LICENSE.txt`. 인터넷 없이 발표 가능.
- UI 참고: 사용자가 설치한 부모 경로 `DESIGN.md`의 여백·정보 위계·부드러운 카드·컨트롤을 참고. 커피 브라운/크림이라는 사용자 색상 지침을 우선.
- PowerPoint: 맑은 고딕·Arial·Georgia. 폰트 파일은 재배포하지 않음. 표지 외 텍스트·표·다이어그램은 수정 가능. 가격·그룹 평균 차트는 네이티브 Office 차트. 9번 그래프는 Seaborn 이미지이므로 데이터 수정은 Python 원본으로 재생성.
