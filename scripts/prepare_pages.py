"""Prepare the self-contained presentation for GitHub Pages, without publishing raw crawls."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1]
D=R/'docs';D.mkdir(exist_ok=True)
(D/'assets').mkdir(exist_ok=True)
shutil.copy2(R/'presentation/index.html',D/'index.html')
for f in (R/'presentation/assets').iterdir():
    if f.is_file():shutil.copy2(f,D/'assets'/f.name)
(D/'.nojekyll').write_text('',encoding='utf-8')
p=R/'README.md';s=p.read_text(encoding='utf-8')
old='공개 배포는 이번 커피 과제에서 요청되지 않아 GitHub 업로드·공개 URL을 만들지 않았다. 로컬 확인: `python -m http.server 8000 --directory presentation`. API 키·인증 파일·가상환경은 제출 ZIP에 포함하지 않는다.'
new='발표 슬라이드: https://ancoded1234.github.io/coffee-brand-analysis/\n\nGitHub 저장소: https://github.com/ancoded1234/coffee-brand-analysis\n\n사용자의 공개 배포 요청에 따라 GitHub CLI와 Pages REST API로 main 브랜치의 /docs를 배포한다. `scripts/prepare_pages.py`로 HTML·로컬 에셋을 복사한다. 원문 크롤링 전문·기존 .env·인증 파일·가상환경은 공개 저장소에서 제외한다. 로컬 확인: `python -m http.server 8000 --directory docs`.'
if old in s:p.write_text(s.replace(old,new),encoding='utf-8')
print('Pages files prepared; raw crawls and credentials excluded')
