"""Data-driven Manim scenes; no LaTeX or fabricated quality scores."""
from pathlib import Path
import json
from manim import *
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'research/reviewed_evidence.json').read_text(encoding='utf-8'))
INK='#30231D';CREAM='#F4EFE6';COCOA='#8A5D43';GREEN='#63765D';MUTED='#9B8E7E'
config.background_color=CREAM
config.pixel_width=1280;config.pixel_height=720;config.frame_rate=24
config.media_dir=str(R/'presentation/assets/manim')
def txt(s,size=26,color=INK):return Text(s,font='Malgun Gothic',font_size=size,color=color)
class PriceComparison(Scene):
    def construct(self):
        self.add(txt('HOT AMERICANO / 공개 가격 관측치',32).to_edge(UP),txt('S04·S08·S10·S12·S14·S17 | 수집 2026.10.18 / 가격 적용일 상이\n텐퍼센트: 울산비즈파크점 · 전국 동시점 평균 아님',14,color=MUTED).to_edge(DOWN))
        self.add(txt('0',18).move_to([-2.6,-2.65,0]),txt('5,000원',18).move_to([4.95,-2.65,0]))
        for i,p in enumerate(D['prices'][:6]):
            y=1.75-i*.73;w=p['기본가격']/5000*7.7
            name=txt(p['브랜드명'],24).move_to([-4.45,y,0]);bar=Rectangle(width=w,height=.38,fill_opacity=1,fill_color=COCOA if i<3 else GREEN,stroke_width=0).move_to([-2.6+w/2,y,0]);val=txt(f"{p['기본가격']:,}",23).next_to(bar,RIGHT,buff=.18)
            self.play(FadeIn(name),GrowFromEdge(bar,LEFT),FadeIn(val),run_time=.65)
        self.wait(2.5)
class DisclosureGap(Scene):
    def construct(self):
        self.add(txt('정보가 없는 칸을 0점으로 읽지 않는다',34).to_edge(UP))
        labels=['품종 비율 확인','국가별 배합비 확보','독립 관능점수 확보'];values=[1,0,0]
        for j,(label,n) in enumerate(zip(labels,values)):
            y=1.6-j*1.6
            self.play(FadeIn(txt(label,26).move_to([-3.5,y,0])),run_time=.4)
            dots=VGroup(*[Circle(radius=.22,stroke_color=COCOA,fill_color=COCOA if i<n else CREAM,fill_opacity=1).move_to([-.1+i*.7,y,0]) for i in range(6)])
            self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=.13),FadeIn(txt(f'{n}/6',25).move_to([4.6,y,0])),run_time=1)
        self.add(txt('S01–S03·S06–S07·S09·S11·S13·S18–S20 | 수집 2026.10.18\n이번 조사에서 확인한 범위 · 미확인은 품질 부재를 의미하지 않음',14,color=MUTED).to_edge(DOWN));self.wait(2.5)
class ValueChain(Scene):
    def construct(self):
        self.add(txt('한 잔의 가격에는 여러 요소가 함께 있다',34).to_edge(UP))
        labels=[('원두','산지·생두·블렌딩'),('제조·관리','로스팅·선별·공급'),('공간','좌석·매장 경험'),('운영·서비스','추출·교육·주문')]
        for i,(a,b) in enumerate(labels):
            x=-4.7+i*3.13
            c=Circle(radius=1.0,stroke_color=COCOA,stroke_width=2,fill_color='#E7D9C8',fill_opacity=1).move_to([x,.4,0]);t=txt(a,25).move_to(c);sub=txt(b,17).move_to([x,-1.2,0])
            self.play(Create(c),FadeIn(t),FadeIn(sub),run_time=.8)
        self.play(FadeIn(txt('각 요소의 원가·마진·기여 비율은 산출하지 않음',26).move_to([0,-2.35,0])),run_time=.6);self.add(txt('S02·S03·S05·S07·S09·S13·S18·S21 | 수집 2026.10.18 | 공식 문구·외부 기업 소개',14,color=MUTED).to_edge(DOWN));self.wait(2)
class EvidenceGap(Scene):
    def construct(self):
        self.add(txt('가격 차이 ≠ 검증된 품질 차이',38).to_edge(UP))
        left=txt('가격\n1,500–4,700원',35).move_to([-3.7,.4,0]);right=txt('독립 품질 비교\n동일 기준 점수 미확보',30).move_to([3.1,.4,0]);arrow=Arrow([-1.2,.4,0],[.8,.4,0],color=COCOA)
        self.play(FadeIn(left),run_time=.8);self.play(GrowArrow(arrow),run_time=.8);self.play(FadeIn(right),run_time=.8)
        self.play(Create(Line([-.5,.9,0],[.2,-.1,0],color='#A4523F',stroke_width=7)),run_time=.5)
        self.play(FadeIn(txt('공개 자료만으로 더 비싼 커피의 원두가 더 좋다고 판정할 수 없다',25).move_to([0,-1.9,0])),run_time=.8);self.add(txt('가격 S04·S08·S10·S12·S14·S17 / 품질 S01–S03·S06–S07·S09·S11·S13·S18–S20\n수집 2026.10.18 · 시점·매장 범위 상이 · 독립 품질 측정값 미확보',14,color=MUTED).to_edge(DOWN));self.wait(2.5)
if __name__=='__main__':
    import shutil
    for cls in [PriceComparison,DisclosureGap,ValueChain,EvidenceGap]:
        scene=cls();scene.render();src=Path(scene.renderer.file_writer.movie_file_path);shutil.copy2(src,R/f'presentation/assets/{cls.__name__}.mp4')
